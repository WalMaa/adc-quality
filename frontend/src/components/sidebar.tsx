import { MessageSquareMore} from "lucide-react";
import React from "react";

export type Response = {
    _id: string;
    system_message: string;
    user_message: string;
    response: string;
};

const fetchResponses = async () => {
    try {
        const res = await fetch("http://localhost:8000/responses");
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        const body: Response[] = await res.json();
        console.log(body);
        return body;
    } catch (error) {
        console.error("Failed to fetch responses:", error);
        return [];
    }
};

export default function Sidebar() {
    const [responses, setResponses] = React.useState<Response[] | []>([]);

    React.useEffect(() => {
        fetchResponses().then((body) => {
            setResponses(body);
        });
    }, []);

    return (
        <aside className="h-full overflow-y-scroll fixed border-r flex flex-col w-64 border-r-gray-600">
            <a href="/" className="w-full p-4 text-white text-left border-b border-gray-600 flex items-center">
                <span className="bg-gray-700 p-2 rounded-full size-8 flex items-center justify-center mr-4">
                    <MessageSquareMore />
                </span>
                <span className="truncate">New Prompt</span>
            </a>
            {responses.map((response, index) => (
                <a
                href={`/responses/${response._id}`}
                    key={response._id}
                    className="w-full p-4 text-white text-left border-b border-gray-600 flex items-center"
                >
                    <span className="bg-gray-700 rounded-full h-8 w-8 flex items-center justify-center mr-4">
                        {index + 1}
                    </span>
                    <div className="flex flex-col w-40">
                        <span className="truncate">
                            {response.user_message}
                        </span>
                        <span className="truncate text-gray-400">
                            {response.system_message}
                        </span>
                    </div>
                </a>
            ))}
        </aside>
    );
}
