import { useState, useEffect } from "react";
import "./App.css";
import PromptForm from "./components/prompt-form";
import Dropdown from "./components/DropDownMenu";

interface DropdownOption {
  value: string;
  label: string;
}

function App() {
    const [systemText, setSystemText] = useState("you are a pirate");
    const [userMessage, setUserMessage] = useState("what is 1+1");
    const [isLoading, setIsLoading] = useState(false);
    const [output, setOutput] = useState("");
    const [llmOptions, setLlmOptions] = useState<DropdownOption[]>([]);
    const [selectedLlm, setSelectedLlm] = useState<DropdownOption | null>(null);

    const handleSystemTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSystemText(e.target.value);
    };

    const handleUserMessageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUserMessage(e.target.value);
    };

    const handleSubmit = async () => {
        setIsLoading(true);
        try {
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
        } catch (error) {
            console.error("Error submitting prompt:", error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
      const fetchLlmOptions = async () => {
        try {
          // Fetch available LLMs
          const response = await fetch("http://localhost:8000/llms/");
          const data = await response.json();
          const options = data.llms.map((llm: { name: string }) => ({
            value: llm.name,
            label: llm.name,
          }));
          setLlmOptions(options);
      
          // Fetch the currently selected LLM
          const selectedResponse = await fetch("http://localhost:8000/llms/selected");
          if (selectedResponse.ok) {
            const selectedData = await selectedResponse.json();
            const selectedOption = options.find(
              (option: { value: string; label: string }) => option.value === selectedData.selected_llm
            );
            setSelectedLlm(selectedOption || null);
          } else {
            console.warn("No model selected on the backend.");
          }
        } catch (error) {
          console.error("Error fetching LLM options or selected LLM:", error);
        }
      };

        fetchLlmOptions();
    }, []);

    const handleLlmSelect = async (option: { value: string; label: string }) => {
        setSelectedLlm(option);
        try {
            const response = await fetch("http://localhost:8000/llms/select", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ model_name: option.value }),
            });
            const data = await response.json();
            console.log(data.message);
        } catch (error) {
            console.error("Error selecting LLM:", error);
        }
    };

    return (
        <div className="w-full mx-auto max-w-md p-4">
            <PromptForm
                isLoading={isLoading}
                userMessage={userMessage}
                systemText={systemText}
                handleSystemTextChange={handleSystemTextChange}
                handleSubmit={handleSubmit}
                handleUserMessageChange={handleUserMessageChange}
            />

            <div className="fixed top-4 right-4">
                {llmOptions.length > 0 && (
                    <Dropdown
                        options={llmOptions}
                        defaultOption={selectedLlm}
                        onSelect={handleLlmSelect}
                    />
                )}
            </div>

            <div className="text-center">
                <h2 className="text-2xl mb-2">Output:</h2>
                <p>{output}</p>
            </div>
        </div>
    );
}

export default App;