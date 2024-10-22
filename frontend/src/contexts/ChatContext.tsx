import React, { useContext, useState, createContext } from "react";

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

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
}

interface ChatContextProps {
  sessions: ChatSession[];
  currentSessionId: string | null;

  createNewSession: () => void;
  deleteSession: (id: string) => void;
  setCurrentSessionId: (id: string) => void;
  updateSessionMessage: (id: string, messages: Message[]) => void;
  getCurrentSession: () => ChatSession | undefined;
}

export const ChatContext = createContext<ChatContextProps | undefined>(
  undefined
);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);

  const createNewSession = () => {
    const newSession: ChatSession = {
      id: Date.now().toString(),
      title: "Chat No: " + (sessions.length + 1),
      messages: [],
      createdAt: new Date(),
    };
    setSessions((prev) => [...prev, newSession]);
    setCurrentSessionId(newSession.id);
  };

  const deleteSession = (id: string) => {
    setSessions((prev) => prev.filter((session) => session.id !== id));
    if (currentSessionId === id) {
      const remainingSessions = sessions.filter((session) => session.id !== id);
      setCurrentSessionId(
        remainingSessions.length > 0 ? remainingSessions[0].id : null
      );
    }
  };

  const updateSessionMessage = (id: string, messages: Message[]) => {
    setSessions((prev) =>
      prev.map((session) =>
        session.id === id ? { ...session, messages } : session
      )
    );
  };

  const getCurrentSession = () => {
    return sessions.find((session) => session.id === currentSessionId);
  };

  return (
    <ChatContext.Provider
      value={{
        sessions,
        currentSessionId,
        createNewSession,
        deleteSession,
        setCurrentSessionId,
        updateSessionMessage,
        getCurrentSession,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChatContext must be used within a ChatProvider");
  }
  return context;
};
