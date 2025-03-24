import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
// import './index.css'
import App from "./App.tsx";
import AppLayout from "./components/AppLayout.tsx";
import ResponsePage from "./ResponsePage.tsx";

createRoot(document.getElementById("root")!).render(
    <StrictMode>
        <BrowserRouter>
        <Routes>
            <Route element={<AppLayout />}>
                <Route path="/" element={<App />} />
                <Route path="/responses/:id" element={<ResponsePage />} />
            </Route>

        </Routes>
        </BrowserRouter>
    </StrictMode>
);
