import { NextResponse } from "next/server";

export async function POST(req: Request) {
    const url = new URL(req.url);
    const docScope = url.searchParams.get("doc_scope") || "default";

    const formData = await req.formData();
    const upstream = await fetch(`http://127.0.0.1:8000/ingest?doc_scope=${encodeURIComponent(docScope)}`, {
        method: "POST",
        body: formData,
    });

    const text = await upstream.text();
    return new NextResponse(text, {
        status: upstream.status,
        headers: { "Content-Type": upstream.headers.get("content-type") || "application/json" },
    });
}
