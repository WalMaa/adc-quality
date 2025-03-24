import { useState } from "react";
import "./App.css";
import "./components/SearchComponent";
import PromptForm from "./components/prompt-form";

function App() {
    const [systemText, setSystemText] = useState("you are a pirate");
    const [userMessage, setUserMessage] = useState("what is 1+1");
    const [isLoading, setIsLoading] = useState(false);
    const [output, setOutput] = useState("");

    const handleSystemTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSystemText(e.target.value);
    };

    const handleUserMessageChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        setUserMessage(e.target.value);
    };

    const handleSubmit = async () => {
        setIsLoading(true);
        const res = await fetch("http://localhost:8000/prompt", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                system_message: systemText,
                user_message: userMessage,
            }),
        });
        const body = await res.json();
        console.log(body);
        setOutput(`${body.response.content}`);
        setIsLoading(false);
    };

    return (
        <div className="w-full container mx-auto max-w-md p-4">
            <PromptForm
                isLoading={isLoading}
                userMessage={userMessage}
                systemText={systemText}
                handleSystemTextChange={handleSystemTextChange}
                handleSubmit={handleSubmit}
                handleUserMessageChange={handleUserMessageChange}
            />

            <div className="text-center">
                <h2 className="text-2xl mb-2">Output:</h2>
                <p>{output}</p>
            </div>
        </div>
    );
}

export default App;
