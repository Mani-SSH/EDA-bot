import React from "react";
import { useSidebar } from "../contexts/SidebarContext";
import { VscLayoutSidebarLeft } from "react-icons/vsc";

const Sidebar: React.FC = () => {
  const { isSidebarOpen, toggleSidebar } = useSidebar();

  return (
    <nav
      className={`flex-col bg-stone-600 text-white p-4 transition-all duration-300 overflow-hidden ${
        isSidebarOpen ? "w-1/4" : "w-20"
      }`}
    >
      <div className="pb-2 flex justify-between items-center">
        <button
          onClick={toggleSidebar}
          className="p-0 bg-stone-600 transition-colors duration-200 ml-auto focus:outline-none"
        >
          <VscLayoutSidebarLeft size={40} />
        </button>
      </div>
    </nav>
  );
};
export default Sidebar;
