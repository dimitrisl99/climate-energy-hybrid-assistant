import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import "./styles.css";

const API_URL = "http://localhost:8000/ask/stream";

const exampleQuestions = [
  "Compare Greece Germany France",
  "What are the main climate risks in Europe?",
  "What are the EU climate neutrality targets?",
  "Compare Greece and Germany emissions and explain what this means.",
];

function splitAnswerAndSources(answer, apiSources) {
  if (apiSources) {
    return {
      cleanAnswer: answer,
      sourceText: apiSources,
    };
  }

  if (!answer?.includes("Sources:")) {
    return {
      cleanAnswer: answer,
      sourceText: "",
    };
  }

  const [cleanAnswer, sourceText] = answer.split("Sources:");

  return {
    cleanAnswer: cleanAnswer.trim(),
    sourceText: sourceText.trim(),
  };
}

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

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

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
      };

      const historyBeforeNewQuestion = messages;

      setMessages((prev) => [
        ...prev,
        userMessage,
        assistantMessage,
      ]);

      setQuestion("");
      setLoading(true);

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

          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n");
          buffer = lines.pop();

          for (const line of lines) {
            if (!line.trim()) continue;

            const event = JSON.parse(line);

            if (event.type === "metadata") {
              setMessages((prev) => {
                const updated = [...prev];
                const lastIndex = updated.length - 1;

                updated[lastIndex] = {
                  ...updated[lastIndex],
                  route: event.route,
                  sources: parseSources(event.sources),
                  rewrittenQuery: event.rewritten_query,
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
          };

          return updated;
        });
      }

      setLoading(false);
    }


   function startNewChat() {
       setMessages([]);
      setQuestion("");
      setLoading(false);
    }

  function handleSubmit(e) {
    e.preventDefault();
    sendQuestion(question);
  }

  return (
    <div className="app">
      <div className="sidebar">
        <h2>🌍 Climate Assistant</h2>

        <p>
          Hybrid AI assistant using:
        </p>

        <ul>
          <li>Structured Analytics</li>
          <li>RAG</li>
          <li>Hybrid Routing</li>
          <li>FastAPI Backend</li>
          <li>Local Qwen LLM</li>
        </ul>

        <div className="memory-box">
          <strong>Memory</strong>
          <span>
            {messages.length} messages
          </span>
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

            <h1>
              Climate Energy Hybrid Assistant
            </h1>

            <p>
              Enterprise-style AI assistant
              for climate and energy intelligence
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
                <ReactMarkdown>
                  {msg.content}
                </ReactMarkdown>
              </div>

              {msg.route && (
                <div className="route-badge">
                  {msg.route}
                </div>
              )}

              {msg.sources?.length > 0 && (
                <details className="sources-panel">
                  <summary>
                    View sources
                  </summary>

                  <div className="sources-list">
                    {msg.sources.map(
                      (source, sourceIndex) => (
                        <div
                          className="source-card"
                          key={sourceIndex}
                        >
                          <div className="source-icon">
                            📄
                          </div>

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
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </details>
              )}

              {msg.rewrittenQuery && (
                <details className="sources-panel">
                  <summary>
                    Rewritten query
                  </summary>

                  <div className="sources-content">
                    {msg.rewrittenQuery}
                  </div>
                </details>
              )}
            </div>
          ))}

          {loading && (
            <div className="loading-card">
              <div className="loader-dot"></div>

              <span>
                Routing query, retrieving
                context, and generating answer...
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
            onChange={(e) =>
              setQuestion(e.target.value)
            }
          />

          <button type="submit">
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;