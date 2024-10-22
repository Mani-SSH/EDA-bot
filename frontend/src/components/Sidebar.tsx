import React, { useEffect } from "react";
import { useState } from "react";
import { useSidebar } from "../contexts/SidebarContext";
import { useChat } from "../contexts/ChatContext";
import { VscLayoutSidebarLeft } from "react-icons/vsc";
import { PlusCircle, MessageSquare, Trash2 } from "lucide-react";

const Sidebar: React.FC = () => {
  const [ShowTitle, setShowTitle] = useState(false);
  const { isSidebarOpen, toggleSidebar } = useSidebar();
  const {
    sessions,
    currentSessionId,
    createNewSession,
    deleteSession,
    setCurrentSessionId,
  } = useChat();

  useEffect(() => {
    if (isSidebarOpen) {
      const timeoutId = setTimeout(() => {
        setShowTitle(true);
      }, 200);

      return () => {
        clearTimeout(timeoutId);
      };
    } else {
      setShowTitle(false);
    }
  }, [isSidebarOpen]);

  return (
    <nav
      className={`flex-col bg-stone-700 text-white p-4 transition-all duration-300 overflow-hidden ${
        isSidebarOpen ? "w-1/4" : "w-20"
      }`}
    >
      <div className="pb-2 flex justify-between items-center border-b border-stone-500">
        {ShowTitle && (
          <div className="flex font-bold text-lg text-stone-300 items-center">
            EDA-bot
          </div>
        )}
        <button
          onClick={toggleSidebar}
          className="p-0 bg-stone-600 hover:bg-stone-600 rounded-lg transition-colors duration-200 ml-auto focus:outline-none"
        >
          <VscLayoutSidebarLeft size={40} className="text-stone-300" />
        </button>
      </div>
      <div className="p-4">
        <button
          onClick={createNewSession}
          className="w-full flex items-center gap-2 p-3 rounded-lg bg-stone-600 hover:bg-stone-500 transition-all duration-200 shadow-md hover:shadow-lg border border-stone-500 hover:border-stone-400"
        >
          <PlusCircle size={20} />
          {isSidebarOpen && <span>New Chat</span>}
        </button>
        <div className="mt-4 space-y-3">
          {sessions.map((session) => (
            <div
              key={session.id}
              className={`
                group flex items-center gap-2 p-3 rounded-lg cursor-pointer
                border shadow-sm hover:shadow-md transition-all duration-200
                ${
                  currentSessionId === session.id
                    ? "bg-stone-500 border-stone-400 shadow-md"
                    : "bg-stone-600 border-stone-500 hover:bg-stone-500 hover:border-stone-400"
                }
              `}
              onClick={() => setCurrentSessionId(session.id)}
            >
              <MessageSquare
                size={20}
                className={
                  currentSessionId === session.id ? "text-blue-300" : ""
                }
              />
              {isSidebarOpen && (
                <span className="flex-1 truncate">{session.title}</span>
              )}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteSession(session.id);
                }}
                className="opacity-0 group-hover:opacity-100 hover:text-red-500 transition-opacity duration-200 p-1 hover:bg-stone-600 rounded"
              >
                <Trash2 size={16} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Sidebar;
