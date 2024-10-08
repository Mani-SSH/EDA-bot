import React, { useEffect, useState } from "react";
import { SlCursor } from "react-icons/sl";

interface Message {
  text: string;
  sender: "user" | "server";
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const BACKEND_URL =
    import.meta.env.REACT_APP_BACKEND_URL || "http://localhost:3000";

  useEffect(() => {
    console.log("Backend URL:", BACKEND_URL);
  }, []);

  const onFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const newMessage: Message = { text: inputMessage, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    try {
      console.log("Sending request to:", `${BACKEND_URL}/send-message`);
      const response = await fetch(`${BACKEND_URL}/send-message`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: inputMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Response from server:", data);

      setMessages((prevMessages) => [
        ...prevMessages,
        { text: data.response, sender: "server" },
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          text: "Error: Unable to reach the server. Please try again later.",
          sender: "server",
        },
      ]);
    }

    setInputMessage("");
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-zinc-400">
      <div className="flex-grow overflow-auto p-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-2 ${
              message.sender === "user" ? "text-right" : "text-left"
            }`}
          >
            <div
              className={`inline-block p-2 rounded-lg ${
                message.sender === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-300 text-black"
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}
      </div>
      <div className="p-4">
        <form
          onSubmit={onFormSubmit}
          className="flex items-center w-full max-w-3xl relative mx-auto"
        >
          <input
            type="text"
            className="w-full px-6 py-4 pr-16 border rounded-full focus:outline-none focus:ring-2 focus:ring-stone-500 bg-stone-300 text-black"
            placeholder="Type your message..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
          />
          <button
            className={`absolute right-1 text-white p-3 rounded-full transition-colors duration-200 ${
              inputMessage.trim()
                ? "bg-stone-600 hover:bg-stone-500"
                : "bg-stone-500"
            }`}
            type="submit"
            disabled={!inputMessage.trim()}
          >
            <SlCursor size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
