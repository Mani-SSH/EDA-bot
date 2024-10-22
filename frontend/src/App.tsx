import Chat from "./components/Chat";
import Sidebar from "./components/Sidebar";
import { SidebarProvider } from "./contexts/SidebarContext";
import { ChatProvider } from "./contexts/ChatContext";

function App() {
  return (
    <SidebarProvider>
      <ChatProvider>
        <div className="flex flex-row h-screen w-screen bg-zinc-400">
          <Sidebar />
          <Chat />
        </div>
      </ChatProvider>
    </SidebarProvider>
  );
}

export default App;
