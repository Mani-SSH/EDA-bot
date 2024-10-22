import Chat from "./components/Chat";
import Sidebar from "./components/Sidebar";
import { SidebarProvider } from "./contexts/SidebarContext";

function App() {
  return (
    <SidebarProvider>
      <div className="flex flex-row h-screen w-screen bg-zinc-400">
        <Sidebar />
        <Chat />
      </div>
    </SidebarProvider>
  );
}

export default App;
