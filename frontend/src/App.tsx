import { useState } from "react";
import "./App.css";
import "./components/SearchComponent";
import { Loader, Loader2 } from "lucide-react";

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
        setOutput(`${body.content}`);
        setIsLoading(false);
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-800 text-white items-center justify-center">
            <header className="text-center mb-8">
                <h1 className="text-2xl font-bold">How can I help?</h1>
            </header>

            <main className="w-full max-w-md p-4">
                <div className="mb-4">
                    <label className="text-2xl block mb-2">System Text:</label>
                    <input
                        type="text"
                        value={systemText}
                        onChange={handleSystemTextChange}
                        className="bg-neutral-700 w-full p-4 mb-4 text-white rounded border border-gray-300"
                    />
                    <label className="text-2xl block mb-2">User Message:</label>
                    <input
                        type="text"
                        value={userMessage}
                        onChange={handleUserMessageChange}
                        className="bg-neutral-700 w-full p-4 mb-4 text-white rounded border border-gray-300 text-lg"
                    />
                    <button
                        onClick={handleSubmit}
                        className="w-full flex bg-blue-500 text-white p-2 rounded"
                    >
                        <span className="mx-auto">
                            {isLoading ? (
                                <Loader2 className=" animate-spin" />
                            ) : (
                                "Submit"
                            )}
                        </span>
                    </button>
                </div>

                <div className="text-center">
                    <h2 className="text-2xl mb-2">Output:</h2>
                    <p>{output}</p>
                </div>
            </main>
        </div>
    );
}

export default App;
