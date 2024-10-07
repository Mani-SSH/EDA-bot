import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const BACKEND_URL =
    import.meta.env.REACT_APP_BACKEND_URL || "http://localhost:3000";

  useEffect(() => {
    fetch(BACKEND_URL)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Fetched message:", data.message); // Log the fetched message
        setMessage(data.message); // Set the message state
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div>
      <h1 style={{ color: "black" }}>{message}</h1> {/* Display the message */}
    </div>
  );
}

export default App;
