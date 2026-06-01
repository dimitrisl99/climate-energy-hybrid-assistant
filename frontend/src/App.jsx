import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./styles.css";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const API_URL = "http://localhost:8000/ask/stream";

const exampleQuestions = [
  "Compare Greece Germany France",
  "Greece CO2 emissions over time",
  "What are the main climate risks in Europe?",
  "What are the EU climate neutrality targets?",
  "Compare Greece and Germany emissions and explain what this means.",
];

function parseSources(sourceText) {
  if (!sourceText) return [];

  return sourceText
    .split("\n")
    .filter((line) => line.trim())
    .map((line) => {
      const pageMatch = line.match(/page\s+(\d+)/i);
      const page = pageMatch ? pageMatch[1] : "N/A";

      const cleaned = line.replace(/^\[\d+\]\s*/, "").trim();
      const parts = cleaned.split("—").map((part) => part.trim());

      return {
        title: parts[0] || "Unknown source",
        page,
        path: parts[2] || parts[1] || "",
        raw: cleaned,
      };
    });
}

function buildPdfUrl(source) {
  if (!source?.path || source.page === "N/A") return null;

  const filename = source.path.split("\\").pop().split("/").pop();

  return `http://localhost:8000/files/${encodeURIComponent(filename)}#page=${source.page}`;
}

function linkifyCitations(content, sources) {
  if (!content || !sources?.length) return content;

  return content.replace(/\[(\d+)\]/g, (match, number) => {
    const source = sources[Number(number) - 1];
    const url = buildPdfUrl(source);

    if (!url) return match;

    return `[${match}](${url})`;
  });
}

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingStatus, setLoadingStatus] = useState("");

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function sendQuestion(text) {
    if (!text.trim()) return;

    const userMessage = {
      role: "user",
      content: text,
    };

    const assistantMessage = {
      role: "assistant",
      content: "",
      route: null,
      sources: [],
      rewrittenQuery: null,
      visualData: [],
      chartType: "bar",
      followUps: [],
    };

    const historyBeforeNewQuestion = messages;

    setMessages((prev) => [
      ...prev,
      userMessage,
      assistantMessage,
    ]);

    setQuestion("");
    setLoading(true);
    setLoadingStatus("Routing query...");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: text,
          chat_history: historyBeforeNewQuestion,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let buffer = "";
      let streamedAnswer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) break;

        buffer += decoder.decode(value, {
          stream: true,
        });

        const lines = buffer.split("\n");
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.trim()) continue;

          const event = JSON.parse(line);

          if (event.type === "status") {
            setLoadingStatus(event.message);
          }

          if (event.type === "metadata") {
            setMessages((prev) => {
              const updated = [...prev];
              const lastIndex = updated.length - 1;

              updated[lastIndex] = {
                ...updated[lastIndex],
                route: event.route,
                sources: parseSources(event.sources),
                rewrittenQuery: event.rewritten_query,
                visualData: event.visual_data || [],
                chartType: event.chart_type || "bar",
                followUps: event.follow_ups || [],
              };

              return updated;
            });
          }

          if (event.type === "token") {
            streamedAnswer += event.content;

            setMessages((prev) => {
              const updated = [...prev];
              const lastIndex = updated.length - 1;

              updated[lastIndex] = {
                ...updated[lastIndex],
                content: streamedAnswer,
              };

              return updated;
            });
          }

          if (event.type === "done") {
            setLoading(false);
            setLoadingStatus("");
          }
        }
      }
    } catch (error) {
      console.error(error);

      setMessages((prev) => {
        const updated = [...prev];
        const lastIndex = updated.length - 1;

        updated[lastIndex] = {
          role: "assistant",
          content: "Something went wrong.",
          sources: [],
          visualData: [],
          chartType: "bar",
          followUps: [],
        };

        return updated;
      });

      setLoadingStatus("");
    }

    setLoading(false);
    setLoadingStatus("");
  }

  function startNewChat() {
    setMessages([]);
    setQuestion("");
    setLoading(false);
    setLoadingStatus("");
  }

  async function downloadReport(msg) {
    const userQuestion =
      [...messages]
        .slice(0, messages.indexOf(msg))
        .reverse()
        .find((item) => item.role === "user")?.content || "";

    const response = await fetch("http://localhost:8000/export-report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: userQuestion,
        answer: msg.content,
        route: msg.route || "",
        sources: msg.sources || [],
        visual_data: msg.visualData || [],
      }),
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "climate_report.pdf";
    a.click();

    window.URL.revokeObjectURL(url);
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendQuestion(question);
  }

  return (
    <div className="app">
      <div className="sidebar">
        <h2>🌍 Climate Assistant</h2>

        <p>Hybrid AI assistant using:</p>

        <ul>
          <li>Structured Analytics</li>
          <li>RAG</li>
          <li>Hybrid Routing</li>
          <li>FastAPI Backend</li>
          <li>Local Qwen LLM</li>
        </ul>

        <div className="memory-box">
          <strong>Memory</strong>
          <span>{messages.length} messages</span>
        </div>

        <button
          type="button"
          className="new-chat-btn"
          onClick={startNewChat}
        >
          + New Chat
        </button>

        <div className="examples-section">
          <h3>Example questions</h3>

          {exampleQuestions.map((example, index) => (
            <button
              key={index}
              className="example-btn"
              onClick={() => sendQuestion(example)}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <div className="chat-container">
        <div className="hero-card">
          <div className="hero-content">
            <span className="hero-label">
              Enterprise AI Assistant
            </span>

            <h1>Climate Energy Hybrid Assistant</h1>

            <p>
              Enterprise-style AI assistant for climate
              and energy intelligence
            </p>
          </div>
        </div>

        <div className="messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.role}`}
            >
              <div className="message-content">
                <ReactMarkdown
                  components={{
                    a: ({ href, children }) => (
                      <a
                        href={href}
                        target="_blank"
                        rel="noreferrer"
                        className="citation-link"
                      >
                        {children}
                      </a>
                    ),
                  }}
                >
                  {msg.role === "assistant"
                    ? linkifyCitations(msg.content, msg.sources)
                    : msg.content}
                </ReactMarkdown>
              </div>

              {msg.route && (
                <div className="route-badge">
                  {msg.route}
                </div>
              )}

              {msg.role === "assistant" && msg.content && (
                <button
                  type="button"
                  className="download-report-btn"
                  onClick={() => downloadReport(msg)}
                >
                  Download Report PDF
                </button>
              )}

              {msg.visualData?.length > 0 && (
                <div className="analytics-panel">
                  <div className="analytics-title">
                    Visual Analytics
                  </div>

                  <div className="analytics-grid">
                    {msg.visualData.map((item, itemIndex) => (
                      <div
                        className="analytics-card"
                        key={itemIndex}
                      >
                        <div className="analytics-country">
                          {item.country || item.year || "Unknown"}
                        </div>

                        <div className="analytics-metric">
                          <span>CO₂</span>
                          <strong>{item.co2 ?? "N/A"}</strong>
                        </div>

                        <div className="analytics-metric">
                          <span>CO₂ / capita</span>
                          <strong>
                            {item.co2_per_capita ?? "N/A"}
                          </strong>
                        </div>

                        <div className="analytics-metric">
                          <span>GHG</span>
                          <strong>{item.ghg ?? "N/A"}</strong>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="chart-section">
                    <div className="chart-title">
                      {msg.chartType === "line"
                        ? "CO₂ emissions trend"
                        : "CO₂ emissions comparison"}
                    </div>

                    <div className="chart-box">
                      <ResponsiveContainer
                        width="100%"
                        height={260}
                      >
                        {msg.chartType === "line" ? (
                          <LineChart data={msg.visualData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="year" />
                            <YAxis />
                            <Tooltip />
                            <Line
                              type="monotone"
                              dataKey="co2"
                              name="CO₂ emissions"
                              stroke="#2563eb"
                              strokeWidth={3}
                              dot={{ r: 4 }}
                              activeDot={{ r: 6 }}
                            />
                          </LineChart>
                        ) : (
                          <BarChart data={msg.visualData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="country" />
                            <YAxis />
                            <Tooltip />
                            <Bar
                              dataKey="co2"
                              name="CO₂ emissions"
                              fill="#2563eb"
                              radius={[8, 8, 0, 0]}
                            />
                          </BarChart>
                        )}
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              )}

              {msg.sources?.length > 0 && (
                <details className="sources-panel">
                  <summary>View sources</summary>

                  <div className="sources-list">
                    {msg.sources.map((source, sourceIndex) => (
                      <div
                        className="source-card"
                        key={sourceIndex}
                      >
                        <div className="source-icon">📄</div>

                        <div className="source-info">
                          <div className="source-title">
                            {source.title}
                          </div>

                          <div className="source-meta">
                            Page {source.page}
                          </div>

                          {source.path && (
                            <div className="source-path">
                              {source.path}
                            </div>
                          )}

                          {buildPdfUrl(source) && (
                            <a
                              className="open-pdf-link"
                              href={buildPdfUrl(source)}
                              target="_blank"
                              rel="noreferrer"
                            >
                              Open PDF
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </details>
              )}

              {msg.rewrittenQuery && (
                <details className="sources-panel">
                  <summary>Rewritten query</summary>

                  <div className="sources-content">
                    {msg.rewrittenQuery}
                  </div>
                </details>
              )}

              {msg.followUps?.length > 0 && (
                <div className="followups-panel">
                  <div className="followups-title">
                    Suggested Questions
                  </div>

                  <div className="followups-grid">
                    {msg.followUps.map((item, followIndex) => (
                      <button
                        key={followIndex}
                        type="button"
                        className="followup-btn"
                        onClick={() => sendQuestion(item)}
                      >
                        {item}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="loading-card">
              <div className="loader-dot"></div>

              <span>
                {loadingStatus || "Processing request..."}
              </span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form
          className="input-form"
          onSubmit={handleSubmit}
        >
          <input
            type="text"
            placeholder="Ask something..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
}

export default App;