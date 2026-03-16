export default function HighlightedText({ text }) {
  return (
    <div style={{ marginTop: 18 }}>
      <h3>Explanation Highlight</h3>
      <p style={{ borderLeft: "3px solid #8ef0b5", paddingLeft: 12 }}>{text}</p>
    </div>
  );
}