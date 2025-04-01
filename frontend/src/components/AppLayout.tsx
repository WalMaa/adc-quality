import { Outlet } from "react-router";
import Sidebar from "./sidebar";

export default function AppLayout() {
    return (
        <div className="flex flex-col min-h-screen h-screen bg-gray-800 text-white items-center justify-center">
            <header className="text-center border-b border-gray-600 p-4 w-full">
                <h1 className="text-2xl font-bold">How can I help?</h1>
            </header>
            <div className="flex h-full w-full">
                    <Sidebar />
                <main className="w-full">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
