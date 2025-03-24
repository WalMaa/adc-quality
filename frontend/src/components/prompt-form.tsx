import { Loader2 } from "lucide-react";

type PromptFormProps = {
    systemText: string;
    userMessage: string;
    isLoading: boolean;
    handleSystemTextChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    handleUserMessageChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    handleSubmit: () => void;
};

export default function PromptForm({
    systemText,
    userMessage,
    isLoading,
    handleSystemTextChange,
    handleUserMessageChange,
    handleSubmit,
}: PromptFormProps) {
    return (
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
                disabled={isLoading}
                onClick={handleSubmit}
                className="w-full flex bg-blue-500 disabled:cursor-not-allowed text-white p-2 rounded"
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
    );
}
