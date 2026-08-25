"use client"

import { getHomeworksByStudentId } from "@/lib/indexedDB";

export default function TestPage() {
    
    const homeworks = getHomeworksByStudentId("1");
    return <div>
        <h1>Test Page</h1>
    </div>
}