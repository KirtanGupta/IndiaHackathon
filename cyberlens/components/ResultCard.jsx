import DeepfakeViewer from "./DeepfakeViewer";
import HighlightedText from "./HighlightedText";
import RiskGauge from "./RiskGauge";
import ShapChart from "./ShapChart";
import { formatRisk } from "../utils/formatRisk";
import { severityColor } from "../utils/severityColor";

export default function ResultCard({ result }) {
  return (
    <section className="panel">
      <h2>Risk Summary</h2>
      <span className="badge" style={{ background: severityColor(result.severity), color: "#08110d" }}>
        {result.severity.toUpperCase()}
      </span>
      <RiskGauge score={result.score} />
      <p>{result.explanation}</p>
      <div className="metric-row">
        <div className="metric">
          <strong>{formatRisk(result.score)}</strong>
          <div>Risk Score</div>
        </div>
        <div className="metric">
          <strong>{result.signals.email_length}</strong>
          <div>Email Length</div>
        </div>
        <div className="metric">
          <strong>{result.signals.media_type}</strong>
          <div>Media Type</div>
        </div>
      </div>
      <HighlightedText text={result.explanation} />
      <ShapChart score={result.score} />
      <DeepfakeViewer mediaType={result.signals.media_type} />
    </section>
  );
}