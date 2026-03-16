export default function DeepfakeViewer({ mediaType }) {
  return (
    <div style={{ marginTop: 18 }}>
      <h3>Media Signal</h3>
      <p>{mediaType === "video" ? "Video frames need enhanced verification." : "Audio waveform appears ready for voice authenticity checks."}</p>
    </div>
  );
}