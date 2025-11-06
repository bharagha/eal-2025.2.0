import { Outlet } from "react-router";
import { Toaster } from "@/components/ui/sonner.tsx";
import FpsDisplay from "@/components/FpsDisplay.tsx";

const Layout = () => {
  return (
    <div>
      {/* remove */}
      <FpsDisplay />
      <Outlet />
      <Toaster position="top-center" richColors />
    </div>
  );
};

export default Layout;
