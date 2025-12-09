import React from "react";

export default function AIContentGenerator() {
  return (
    <div className="w-full min-h-screen bg-[#0b0f19] text-white p-6 flex justify-center">
      <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* LEFT PANEL */}
        <div className="bg-[#111827] p-6 rounded-2xl shadow-xl space-y-6">
          <h2 className="text-2xl font-semibold">AI Content Generator</h2>
          <p className="text-gray-400 text-sm">
            Create and assign educational content powered by AI.
          </p>

          <div className="space-y-4">
            {/* Content Type */}
            <div>
              <label className="text-sm text-gray-300">Content Type</label>
              <select className="w-full mt-1 p-2 rounded-lg bg-[#1f2937] border border-gray-700">
                <option>Quiz Questions</option>
                <option>Summary</option>
                <option>Flashcards</option>
              </select>
            </div>

            {/* Difficulty */}
            <div>
              <label className="text-sm text-gray-300">Difficulty Level</label>
              <select className="w-full mt-1 p-2 rounded-lg bg-[#1f2937] border border-gray-700">
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>
            </div>

            {/* Content Length */}
            <div>
              <label className="text-sm text-gray-300">Content Length</label>
              <input type="range" className="w-full" />
            </div>

            {/* Custom Prompt */}
            <div>
              <label className="text-sm text-gray-300">Custom Prompts</label>
              <textarea
                className="w-full mt-1 p-2 rounded-lg bg-[#1f2937] border border-gray-700 h-20"
                placeholder="e.g. 'Focus on the industrial revolution...'"
              />
            </div>

            {/* Buttons */}
            <div className="flex gap-3 pt-2">
              <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg">
                Generate Content
              </button>
              <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg">
                Reset
              </button>
            </div>
          </div>
        </div>

        {/* RIGHT PANEL */}
        <div className="bg-[#111827] p-6 rounded-2xl shadow-xl">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold">Live Preview</h3>
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg">
              Assign
            </button>
          </div>

          <div className="space-y-6">
            {/* Question 1 */}
            <div className="border border-gray-700 rounded-xl p-4 bg-[#1a2332]">
              <h4 className="font-semibold mb-2">Question 1: Multiple Choice</h4>
              <p className="text-gray-300 mb-2">
                What was the primary innovation that sparked the Industrial Revolution?
              </p>

              <div className="space-y-1 text-gray-400">
                <p>A) The printing press</p>
                <p className="bg-blue-900/40 p-1 rounded">B) The steam engine</p>
                <p>C) The internet</p>
                <p>D) The telescope</p>
              </div>
            </div>

            {/* Question 2 */}
            <div className="border border-gray-700 rounded-xl p-4 bg-[#1a2332]">
              <h4 className="font-semibold mb-2">Question 2: True or False</h4>
              <p className="text-gray-300 mb-2">
                The Industrial Revolution began in the United States.
              </p>

              <div className="flex gap-3 text-gray-400">
                <p>True</p>
                <p className="bg-blue-900/40 p-1 rounded">False</p>
              </div>
            </div>

            {/* Question 3 */}
            <div className="border border-gray-700 rounded-xl p-4 bg-[#1a2332]">
              <h4 className="font-semibold mb-2">Question 3: Fill in the Blank</h4>
              <p className="text-gray-300 mb-2">
                The ________ system was a new method of manufacturing that became
                common during the Industrial Revolution.
              </p>
              <p className="text-green-400 text-sm">Correct Answer: factory</p>
            </div>
          </div>

          <div className="mt-6 text-gray-500 text-sm text-center">
            Generated content will appear here.
          </div>
        </div>
      </div>
    </div>
  );
}
