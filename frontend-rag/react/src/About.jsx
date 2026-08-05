import { useState } from "react";

const techStack = [
  "nvidia/llama-nemotron-embed-1b-v2",
  "langgraph",
  "milvus",
  "OpenAI",
  "FastAPI",
  "Node.js & React",
  "Docker",
  "AWS",
];

const supportedLanguages = [
  { name: "English", flag: "🇺🇸" },
  { name: "Arabic", flag: "🇸🇦" },
  { name: "Bengali", flag: "🇧🇩" },
  { name: "Chinese", flag: "🇨🇳" },
  { name: "Czech", flag: "🇨🇿" },
  { name: "Danish", flag: "🇩🇰" },
  { name: "Dutch", flag: "🇳🇱" },
  { name: "Finnish", flag: "🇫🇮" },
  { name: "French", flag: "🇫🇷" },
  { name: "German", flag: "🇩🇪" },
  { name: "Hebrew", flag: "🇮🇱" },
  { name: "Hindi", flag: "🇮🇳" },
  { name: "Hungarian", flag: "🇭🇺" },
  { name: "Indonesian", flag: "🇮🇩" },
  { name: "Italian", flag: "🇮🇹" },
  { name: "Japanese", flag: "🇯🇵" },
  { name: "Korean", flag: "🇰🇷" },
  { name: "Norwegian", flag: "🇳🇴" },
  { name: "Persian (Farsi)", flag: "🇮🇷" },
  { name: "Polish", flag: "🇵🇱" },
  { name: "Portuguese", flag: "🇵🇹" },
  { name: "Russian", flag: "🇷🇺" },
  { name: "Spanish", flag: "🇪🇸" },
  { name: "Swedish", flag: "🇸🇪" },
  { name: "Thai", flag: "🇹🇭" },
  { name: "Turkish", flag: "🇹🇷" },
];

function About({ onBack }) {
  const [showAllLanguages, setShowAllLanguages] = useState(false);

  const visibleLanguages = showAllLanguages
    ? supportedLanguages
    : supportedLanguages.slice(0, 10);

  return (
    <div className="page-transition about-view">
      <section className="hero-panel about-hero">
        <div className="hero-copy">
          <p className="eyebrow">About</p>
          <h2>Built for multilingual, grounded retrieval workflows.</h2>
          <p className="hero-text">
            This page highlights the stack behind the agentic RAG experience and the
            language coverage supported by the current setup.
          </p>
        </div>

        <div className="hero-stats">
          <div className="stat-card">
            <span className="stat-label">Tech stack</span>
            <strong className="stat-value">8 core components</strong>
          </div>

          <div className="stat-card stat-card-muted">
            <span className="stat-label">Supported languages</span>
            <strong className="stat-value">26 languages</strong>
          </div>
        </div>
      </section>

      <section className="about-grid">
        <article className="panel-card about-card">
          <div className="panel-head">
            <div>
              <p className="panel-kicker">Platform</p>
              <h2>Tech stack</h2>
            </div>
          </div>

          <div className="tech-stack-grid">
            {techStack.map((item) => (
              <div className="collection-chip tech-chip" key={item}>
                {item}
              </div>
            ))}
          </div>
        </article>

        <article className="panel-card about-card">
          <div className="panel-head about-panel-head">
            <div>
              <p className="panel-kicker">Coverage</p>
              <h2>Supported languages</h2>
            </div>

            <button
              type="button"
              className="secondary-button"
              onClick={() => setShowAllLanguages((prev) => !prev)}
            >
              {showAllLanguages ? "Show less" : "Show more"}
            </button>
          </div>

          <div className="language-table-wrap">
            <table className="language-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Language</th>
                </tr>
              </thead>
              <tbody>
                {visibleLanguages.map((language, index) => (
                  <tr key={language.name}>
                    <td>{index + 1}</td>
                    <td>
                      {language.name} <span className="language-flag">{language.flag}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <p className="panel-note">
            Toggle the list to view a compact summary or the full multilingual support set.
          </p>
        </article>
      </section>

      <div className="about-footer-actions">
        <button type="button" className="primary-button" onClick={onBack}>
          Back to Home
        </button>
      </div>
    </div>
  );
}

export default About;
