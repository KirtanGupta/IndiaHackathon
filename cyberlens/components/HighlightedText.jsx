export default function HighlightedText({ text }) {
  return (
    <div style={{ marginTop: 18 }}>
      <h3>Phase Explanation</h3>
      <p style={{ borderLeft: "3px solid #8ef0b5", paddingLeft: 12 }}>{text}</p>
    </div>
  );
}