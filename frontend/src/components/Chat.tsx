// components/Chat.tsx
import React, { useState } from "react";
import { SlCursor } from "react-icons/sl";
import { useSidebar } from "../contexts/SidebarContext";
import { useChat } from "../contexts/ChatContext";

interface Message {
  text: string;
  sender: "user" | "server";
  keywords?: string[];
  showEDAPrompt?: boolean;
}

const Chat = () => {
  const [inputMessage, setInputMessage] = useState("");
  const { isSidebarOpen } = useSidebar();
  const {
    currentSessionId,
    getCurrentSession,
    updateSessionMessage,
    createNewSession,
  } = useChat();

  const BACKEND_URL =
    import.meta.env.REACT_APP_BACKEND_URL || "http://localhost:3000";
  const STREAMLIT_URL =
    import.meta.env.REACT_APP_STREAMLIT_URL || "http://localhost:8501";

  const currentSession = getCurrentSession();

  // Create a new session if none exists
  React.useEffect(() => {
    if (!currentSession) {
      createNewSession();
    }
  }, [currentSession, createNewSession]);

  const openStreamlit = () => {
    window.open(STREAMLIT_URL, "_blank");
  };

  const onFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!inputMessage.trim() || !currentSessionId) return;

    const newMessage: Message = { text: inputMessage, sender: "user" };
    const updatedMessages = [...(currentSession?.messages || []), newMessage];
    updateSessionMessage(currentSessionId, updatedMessages);

    try {
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
      const serverMessage: Message = {
        text: data.response,
        sender: "server",
        keywords: data.keywords,
        showEDAPrompt: data.is_eda_related,
      };

      updateSessionMessage(currentSessionId, [
        ...updatedMessages,
        serverMessage,
      ]);
    } catch (error) {
      console.error("Error sending message:", error);
      updateSessionMessage(currentSessionId, [
        ...updatedMessages,
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
    if (currentSessionId && currentSession) {
      const updatedMessages = currentSession.messages.map((msg, i) =>
        i === index ? { ...msg, showEDAPrompt: false } : msg
      );
      updateSessionMessage(currentSessionId, updatedMessages);
    }
  };

  const renderMessageText = (text: string) => {
    return { __html: text };
  };

  if (!currentSession) return null;

  return (
    <div
      className={`flex flex-col transition-all duration-300 ${
        isSidebarOpen ? "w-3/4" : "w-full"
      }`}
    >
      <div className="flex-grow overflow-auto p-10">
        {currentSession.messages.map((message, index) => (
          <div
            key={index}
            className={`mb-2 ${
              message.sender === "user" ? "text-right" : "text-left"
            }`}
          >
            <div
              className={`inline-block p-2 rounded-md font ${
                message.sender === "user"
                  ? "bg-stone-700 text-white"
                  : "bg-gray-300 text-black"
              }`}
            >
              <div dangerouslySetInnerHTML={renderMessageText(message.text)} />
              {message.showEDAPrompt && (
                <div className="mt-2 p-3 bg-stone-400 rounded-lg text-black">
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
      <div className="p-5">
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
};

export default Chat;
