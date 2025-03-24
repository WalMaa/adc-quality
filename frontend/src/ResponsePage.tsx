import React from 'react'
import { useParams } from "react-router";
import { Response } from './components/sidebar';

const getResponse = async (id: string): Promise<Response> => {
    const res = await fetch(`http://localhost:8000/responses/${id}`);
    const body = await res.json();
    return body;
}

export default function ResponsePage() {
    const [response, setResponse] = React.useState<Response | null>(null);

    const { id } = useParams();

    React.useEffect(() => {
        getResponse(id!).then((body) => {
            console.log(body);
            setResponse(body);
        });
    }, [id]);



return (
    <div className="flex justify-center items-center container mx-auto">
        {response ? (
            <div className="p-6 rounded-lg shadow-md max-w-xl w-full">
                <h1 className="text-2xl mb-4">System Message:</h1>
                <p className="text-lg mb-2">{response.system_message}</p>
                <h2 className="text-xl mb-4">User Message:</h2>
                <p className="text-lg mb-2">{response.user_message}</p>
                <h3 className="text-lg mb-4">Response:</h3>
                <p className="text-base text-gray-200">{response.response}</p>
            </div>
        ) : (
            <p className="text-lg text-gray-500">Loading...</p>
        )}
    </div>
)
}
