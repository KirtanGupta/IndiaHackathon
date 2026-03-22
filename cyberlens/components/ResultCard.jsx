import DeepfakeViewer from "./DeepfakeViewer";
import HighlightedText from "./HighlightedText";
import RiskGauge from "./RiskGauge";
import ShapChart from "./ShapChart";
import { formatRisk } from "../utils/formatRisk";
import { severityColor } from "../utils/severityColor";

export default function ResultCard({ result, activePhase }) {
  const activeModule = result.modules?.[activePhase];
  const severity = result.severity || "low";

  return (
    <section className="panel">
      <h2>Risk Summary</h2>
      <span className="badge" style={{ background: severityColor(severity), color: "#08110d" }}>
        {severity.toUpperCase()}
      </span>
      <RiskGauge score={result.score || 0} />
      <p>{result.explanation || "Run a phase to see isolated analysis."}</p>
      <div className="metric-row">
        <div className="metric">
          <strong>{formatRisk(result.score || 0)}</strong>
          <div>{activePhase} Risk</div>
        </div>
        <div className="metric">
          <strong>{activeModule ? formatRisk(activeModule.score || 0) : "-"}</strong>
          <div>Active Module</div>
        </div>
        <div className="metric">
          <strong>{activeModule?.source || "-"}</strong>
          <div>Decision Source</div>
        </div>
      </div>
      <HighlightedText text={activeModule ? result.module_explanations?.[activePhase] || "" : result.explanation || ""} />
      <ShapChart modules={[activeModule].filter(Boolean)} />
      {activePhase === "deepfake" ? <DeepfakeViewer mediaType={result.signals?.media_type || "audio"} /> : null}
    </section>
  );
}