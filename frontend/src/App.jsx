import "./styles.css";
import { useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async (customQuestion = null) => {
    const finalQuestion = customQuestion || question;

    if (!finalQuestion.trim()) return;

    const userMessage = {
      role: "user",
      content: finalQuestion,
    };

    setMessages((prev) => [...prev, userMessage]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/ask/stream",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: finalQuestion,
            chat_history: messages,
          }),
        }
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantMessage = {
        role: "assistant",
        content: "",
        route: "",
        sources: "",
        rewrittenQuery: "",
        visualData: [],
      };

      setMessages((prev) => [...prev, assistantMessage]);

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter(Boolean);

        for (const line of lines) {
          const event = JSON.parse(line);

          if (event.type === "metadata") {
            assistantMessage.route = event.route;
            assistantMessage.sources = event.sources;
            assistantMessage.rewrittenQuery =
              event.rewritten_query;
            assistantMessage.visualData =
              event.visual_data || [];

            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                ...assistantMessage,
              };
              return updated;
            });
          }

          if (event.type === "token") {
            assistantMessage.content += event.content;

            setMessages((prev) => {
              const updated = [...prev];
              updated[updated.length - 1] = {
                ...assistantMessage,
              };
              return updated;
            });
          }
        }
      }
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong.",
        },
      ]);
    }

    setLoading(false);
  };

  const exampleQuestions = [
    "Compare Greece Germany France",
    "What are the main climate risks in Europe?",
    "What are the EU climate neutrality targets?",
    "Compare Greece and Germany emissions and explain what this means.",
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-header">
          🌍 Climate Assistant
        </div>

        <div className="sidebar-section">
          <div className="sidebar-title">
            Hybrid AI assistant using:
          </div>

          <ul className="feature-list">
            <li>Structured Analytics</li>
            <li>RAG</li>
            <li>Hybrid Routing</li>
            <li>FastAPI Backend</li>
            <li>Local Qwen LLM</li>
          </ul>
        </div>

        <div className="memory-box">
          <div className="memory-title">Memory</div>
          <div className="memory-count">
            {messages.length} messages
          </div>
        </div>

        <button
          className="new-chat-button"
          onClick={() => setMessages([])}
        >
          + New Chat
        </button>

        <div className="sidebar-section">
          <div className="sidebar-title">
            Example questions
          </div>

          <div className="examples">
            {exampleQuestions.map((q) => (
              <button
                key={q}
                className="example-button"
                onClick={() => askQuestion(q)}
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </aside>

      <main className="main">
        <div className="hero">
          <div className="hero-badge">
            Enterprise AI Assistant
          </div>

          <h1>
            Climate Energy Hybrid Assistant
          </h1>

          <p>
            Enterprise-style AI assistant for climate
            and energy intelligence
          </p>
        </div>

        <div className="chat-container">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.role}`}
            >
              <div className="message-bubble">
                <div className="message-content">
                  {msg.content}
                </div>
              </div>

              {msg.role === "assistant" && (
                <>
                  {msg.route && (
                    <div className="route-badge">
                      {msg.route.toUpperCase()}
                    </div>
                  )}

                  {msg.visualData?.length > 0 && (
                    <div className="analytics-panel">
                      <div className="analytics-title">
                        Visual Analytics
                      </div>

                      <div className="analytics-grid">
                        {msg.visualData.map((item) => (
                          <div
                            key={item.country}
                            className="analytics-card"
                          >
                            <div className="analytics-country">
                              {item.country}
                            </div>

                            <div className="analytics-row">
                              <span>CO₂</span>
                              <strong>
                                {item.co2 ?? "N/A"}
                              </strong>
                            </div>

                            <div className="analytics-row">
                              <span>CO₂ / capita</span>
                              <strong>
                                {item.co2_per_capita ??
                                  "N/A"}
                              </strong>
                            </div>

                            <div className="analytics-row">
                              <span>GHG</span>
                              <strong>
                                {item.ghg ?? "N/A"}
                              </strong>
                            </div>
                          </div>
                        ))}
                      </div>

                      <div className="chart-section">
                        <div className="chart-title">
                          CO₂ emissions comparison
                        </div>

                        <div className="chart-box">
                          <ResponsiveContainer
                            width="100%"
                            height={260}
                          >
                            <BarChart
                              data={msg.visualData}
                            >
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
                          </ResponsiveContainer>
                        </div>
                      </div>
                    </div>
                  )}

                  {msg.sources && (
                    <details className="sources-box">
                      <summary>
                        View sources
                      </summary>

                      <pre>{msg.sources}</pre>
                    </details>
                  )}

                  {msg.rewrittenQuery && (
                    <details className="rewrite-box">
                      <summary>
                        Rewritten query
                      </summary>

                      <div>
                        {msg.rewrittenQuery}
                      </div>
                    </details>
                  )}
                </>
              )}
            </div>
          ))}

          {loading && (
            <div className="loading">
              Thinking...
            </div>
          )}
        </div>

        <div className="input-container">
          <input
            type="text"
            placeholder="Ask something..."
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askQuestion();
              }
            }}
          />

          <button onClick={() => askQuestion()}>
            Send
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;