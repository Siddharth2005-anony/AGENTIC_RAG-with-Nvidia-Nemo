import { useRef, useState } from "react";
import axios from "axios";
import About from "./About";
import "./App.css";

const API = "/api";

function formatDuration(ms) {
  if (!Number.isFinite(ms)) return null;
  if (ms < 1000) return `${Math.round(ms)} ms`;
  return `${(ms / 1000).toFixed(2)} s`;
}

function App() {
  const [currentPage, setCurrentPage] = useState("home");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [collections, setCollections] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [isThinking, setIsThinking] = useState(false);

  const fileInputRef = useRef(null);

  const sendQuery = async () => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery || isThinking) return;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: trimmedQuery,
      },
    ]);

    setIsThinking(true);

    const startedAt = performance.now();

    try {
      const res = await axios.post(`${API}/NVIDIA`, {
        query: trimmedQuery,
      });

      const totalMs = performance.now() - startedAt;

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: res.data.answer,
          metrics: {
            totalMs,
          },
        },
      ]);
    } catch (err) {
      console.log(err);

      const totalMs = performance.now() - startedAt;

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "The request failed. Check the backend connection and try again.",
          error: true,
          metrics: {
            totalMs,
          },
        },
      ]);
    } finally {
      setIsThinking(false);
      setQuery("");
    }
  };

  const getCollections = async () => {
    try {
      const res = await axios.get(`${API}/collections`);
      setCollections(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const uploadFile = async () => {
    if (!fileInputRef.current?.files?.[0]) return;

    const file = fileInputRef.current.files[0];
    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setUploadStatus("Uploading...");

    try {
      const startedAt = performance.now();
      const res = await axios.post(`${API}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const totalMs = performance.now() - startedAt;

      setUploadStatus(
        `Uploaded: ${res.data.filename} (${res.data.chunks} chunks) in ${formatDuration(totalMs)}`
      );
      fileInputRef.current.value = "";
    } catch (err) {
      setUploadStatus(`Error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleComposerKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendQuery();
    }
  };

  const lastLatency = [...messages]
    .reverse()
    .find((message) => message.sender === "bot" && message.metrics?.totalMs)?.metrics?.totalMs;

  return (
    <main className="app-shell">
      <header className="top-nav">
        <div>
          <p className="eyebrow">Agentic Retrieval Demo</p>
        </div>

        <div className="nav-actions">
          <button
            type="button"
            className={`nav-button ${currentPage === "home" ? "nav-button-active" : ""}`}
            onClick={() => setCurrentPage("home")}
          >
            Home
          </button>
          <button
            type="button"
            className={`nav-button ${currentPage === "about" ? "nav-button-active" : ""}`}
            onClick={() => setCurrentPage("about")}
          >
            About
          </button>
        </div>
      </header>

      {currentPage === "home" ? (
        <div className="page-transition" key="home">
          <section className="hero-panel">
            <div className="hero-copy">
              <p className="eyebrow">Agentic Retrieval Demo</p>
              <h2>Agentic RAG pipeline in "Enterprise" level.</h2>
              <p className="hero-text">
                An end-to-end retrieval-augmented AI assistant featuring semantic
                search, vector retrieval, and grounded responses. Supported upto 26
                Languages.
              </p>
            </div>

            <div className="hero-stats">
              <div className="stat-card">
                <span className="stat-label">Latest response</span>
                <strong className="stat-value">
                  {lastLatency ? formatDuration(lastLatency) : "Waiting for first query"}
                </strong>
              </div>

              
            </div>
          </section>

          <section className="workspace-grid">
            <aside className="side-panel">
              <div className="panel-card">
                <div className="panel-head">
                  <div>
                    <p className="panel-kicker">Knowledge Base</p>
                    <h2>Upload Documents</h2>
                  </div>
                  <span className={`status-pill ${uploading ? "status-live" : ""}`}>
                    {uploading ? "Uploading" : "Ready"}
                  </span>
                </div>

                <input
                  type="file"
                  ref={fileInputRef}
                  accept=".pdf,.txt,.docx"
                  onChange={uploadFile}
                  className="hidden-input"
                  id="file-upload"
                />

                <label htmlFor="file-upload" className="upload-trigger">
                  <span className="upload-icon">+</span>
                  <span>Select a file</span>
                </label>

                <p className="panel-note">Supported formats: PDF, TXT, DOCX.</p>

                {uploadStatus && (
                  <div
                    className={`feedback-banner ${
                      uploadStatus.startsWith("Error:") ? "feedback-error" : "feedback-ok"
                    }`}
                  >
                    {uploadStatus}
                  </div>
                )}
              </div>

              <div className="panel-card">
                <div className="panel-head">
                  <div>
                    <p className="panel-kicker">Storage</p>
                    <h2>Collections</h2>
                  </div>
                  <button type="button" className="secondary-button" onClick={getCollections}>
                    Refresh
                  </button>
                </div>

                <div className="collection-list">
                  {collections.length > 0 ? (
                    collections.map((item, index) => (
                      <div className="collection-chip" key={`${item}-${index}`}>
                        {item}
                      </div>
                    ))
                  ) : (
                    <p className="empty-copy">No collections loaded yet.</p>
                  )}
                </div>
              </div>
            </aside>

            <section className="chat-panel">
              <div className="chat-header">
                <div>
                  <p className="panel-kicker">Conversation</p>
                  <h2>Ask the assistant</h2>
                </div>
                <span className={`status-pill ${isThinking ? "status-live" : ""}`}>
                  {isThinking ? "Working" : "Idle"}
                </span>
              </div>

              <div className="message-stream">
                {messages.length > 0 ? (
                  messages.map((msg, index) => (
                    <article
                      key={index}
                      className={`message-row ${
                        msg.sender === "user" ? "message-user" : "message-bot"
                      } ${msg.error ? "message-error" : ""}`}
                    >
                      <div className="message-badge">
                        {msg.sender === "user" ? "You" : "Agent"}
                      </div>

                      <div className="message-card">
                        <p className="message-text">{msg.text}</p>

                        {msg.sender === "bot" && msg.metrics?.totalMs ? (
                          <div className="latency-card">
                            <div>
                              <span className="latency-label">Latency</span>
                              <strong className="latency-value">
                                Total time: {formatDuration(msg.metrics.totalMs)}
                              </strong>
                            </div>
                            <span className="latency-note">
                              Server-stage timings are not exposed by this API.
                            </span>
                          </div>
                        ) : null}
                      </div>
                    </article>
                  ))
                ) : (
                  <div className="empty-state">
                    <p className="empty-title">No conversation yet</p>
                    <p className="empty-copy">
                      Ask a question to see the response and its real round-trip time.
                    </p>
                    <p className="empty-copy">
                      For eg: capital of tokyo? When do the cherry blossoms bloom?etc..
                    </p>
                  </div>
                )}

                {isThinking ? (
                  <article className="message-row message-bot">
                    <div className="message-badge">Agent</div>
                    <div className="message-card message-card-pending">
                      <p className="message-text">Searching the knowledge base...</p>
                    </div>
                  </article>
                ) : null}
              </div>

              <div className="composer">
                <textarea
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  onKeyDown={handleComposerKeyDown}
                  placeholder="Ask something about your documents..."
                  rows={3}
                />

                <button
                  type="button"
                  className="primary-button"
                  onClick={sendQuery}
                  disabled={isThinking}
                >
                  {isThinking ? "Thinking..." : "Submit"}
                </button>
              </div>
            </section>
          </section>
        </div>
      ) : (
        <About onBack={() => setCurrentPage("home")} />
      )}
    </main>
  );
}

export default App;
