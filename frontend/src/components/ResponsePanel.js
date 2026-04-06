import Card from "./Card";

function ResponsePanel({ error, responseData }) {
  return (
    <>
      {error && <p className="error-banner">{error}</p>}
      <Card title="API Response">
        <pre>{JSON.stringify(responseData, null, 2) || "Run an action to view response."}</pre>
      </Card>
    </>
  );
}

export default ResponsePanel;
