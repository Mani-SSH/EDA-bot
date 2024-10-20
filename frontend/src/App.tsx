import React, { useState } from "react";
import { SlCursor } from "react-icons/sl";

/**
 * Represents the structure of a message exchanged between the user and the server.
 *
 * @property {string} text - The content of the message.
 * @property {"user" | "server"} sender - The sender of the message, either "user" or "server".
 * @property {string[]} [keywords] - Optional array of keywords related to the message (if any).
 * @property {boolean} [showEDAPrompt] - Optional flag indicating whether to show a prompt
 *                                       for Exploratory Data Analysis (EDA) based on the message content.
 */
interface Message {
  text: string;
  sender: "user" | "server";
  keywords?: string[];
  showEDAPrompt?: boolean;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]); // Array of message of type Message
  const [inputMessage, setInputMessage] = useState(""); // Messages from the user input
  const BACKEND_URL =
    import.meta.env.REACT_APP_BACKEND_URL || "http://localhost:3000";
  const STREAMLIT_URL =
    import.meta.env.REACT_APP_STREAMLIT_URL || "http://localhost:8501";

  /**
   * Opens new tab to the Streamlit URL for the EDA processes
   */
  const openStreamlit = () => {
    window.open(STREAMLIT_URL, "_blank");
  };

  /**
   * On submitting the Form:
   * Message will have sender: user
   * Message will be sent to the server, and response is gathered
   * Gathered response will have sender: server
   */
  const onFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const newMessage: Message = { text: inputMessage, sender: "user" }; // creating new message of type Message with text as user input and sender: user
    setMessages((prevMessages) => [...prevMessages, newMessage]); // adds newMessage to end of array prevMessages

    try {
      console.log("Sending request to:", `${BACKEND_URL}/send-message`); //checking the url before fetching

      /**
       * Sends a POST request to the server to send a message.
       * The request is sent to the URL constructed from BACKEND_URL and the endpoint '/send-message'.
       * The body contains the message, which is converted to a JSON string.
       */
      const response = await fetch(`${BACKEND_URL}/send-message`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: inputMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`); // if response has an error
      }

      const data = await response.json();
      console.log("Response from server:", data.response); // logging response from the server\

      const serverMessage: Message = {
        text: data.response,
        sender: "server",
        keywords: data.keywords,
        showEDAPrompt: data.is_eda_related,
      };

      setMessages((prevMessages) => [...prevMessages, serverMessage]);
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

  const handleEDAResponse = (accept: boolean, index: number) => {
    if (accept) {
      openStreamlit();
    }
    setMessages((prevMessages) =>
      prevMessages.map((msg, i) =>
        i === index ? { ...msg, showEDAPrompt: false } : msg
      )
    );
  };

  const renderMessageText = (text: string) => {
    return { __html: text };
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
                  ? "bg-stone-700 text-white"
                  : "bg-gray-300 text-black"
              }`}
            >
              <div dangerouslySetInnerHTML={renderMessageText(message.text)} />
              {message.showEDAPrompt && (
                <div className="mt-2">
                  <p>
                    Would you like to use our Streamlit interface for these
                    operations?
                  </p>
                  <div className="mt-2">
                    <button
                      onClick={() => handleEDAResponse(true, index)}
                      className="bg-stone-600 text-white px-4 py-2 rounded mr-2 hover:bg-stone-400 transition-colors duration-200"
                    >
                      Yes
                    </button>
                    <button
                      onClick={() => handleEDAResponse(false, index)}
                      className="bg-stone-600 text-white px-4 py-2 rounded hover:bg-stone-400 transition-colors duration-200"
                    >
                      No
                    </button>
                  </div>
                </div>
              )}
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
