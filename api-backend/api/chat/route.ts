import { NextResponse } from "next/server";

export async function POST(req: Request) {
    const body = await req.text();
    const upstream = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
    });

    const text = await upstream.text();
    return new NextResponse(text, {
        status: upstream.status,
        headers: { "Content-Type": upstream.headers.get("content-type") || "application/json" },
    });
}
