import React from "react";

export default function AssignmentDetail() {
  return (
    <div className="min-h-screen bg-[#0b0c10] text-white p-8 font-sans">
      {/* Top Navigation */}
      <header className="flex justify-between items-center mb-8">
        <div className="text-lg font-bold">AMEP</div>
        <nav className="flex items-center gap-6 text-gray-300">
          <button className="hover:text-white">Courses</button>
          <button className="hover:text-white">Assignments</button>
          <button className="hover:text-white">Profile</button>
          <button className="bg-teal-500 px-4 py-2 rounded-lg text-black font-semibold">Logout</button>
        </nav>
      </header>

      {/* Breadcrumb */}
      <p className="text-gray-500 text-sm mb-4">
        Courses / CS 101 / Assignments / <span className="text-gray-300">Generative Art with p5.js</span>
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        {/* Left Section */}
        <div>
          <h1 className="text-4xl font-bold leading-tight mb-2">Assignment: Generative Art with p5.js</h1>
          <p className="text-gray-400 text-sm mb-6">
            Due: Dec 15, 2024 | <span className="text-yellow-400">In Progress</span> | 100 Points
          </p>

          {/* Description Box */}
          <div className="bg-[#121318] p-6 rounded-2xl shadow-lg mb-8">
            <h2 className="text-xl font-semibold mb-3">Description</h2>
            <p className="text-gray-300 leading-relaxed">
              This assignment challenges you to create a dynamic, interactive piece of generative art using the p5.js
              library. Explore concepts of randomness, loops, and user input to build a unique visual experience. The
              goal is to apply fundamental programming concepts in a creative context.
            </p>
          </div>

          {/* Learning Objectives */}
          <h2 className="text-2xl font-semibold mb-4">Learning Objectives</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {[{
              title: "p5.js Basics",
              desc: "Understand the setup and draw loops."
            },{
              title: "Interactivity",
              desc: "Use mouse and keyboard inputs."
            },{
              title: "Randomness",
              desc: "Implement random functions for variety."
            },{
              title: "Color Theory",
              desc: "Apply color to create mood and focus."
            }].map((obj, i) => (
              <div key={i} className="bg-[#0f1115] p-5 rounded-xl border border-gray-800">
                <h3 className="font-semibold text-lg mb-2">{obj.title}</h3>
                <p className="text-gray-400 text-sm">{obj.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Section: Workspace */}
        <div className="bg-[#121318] p-6 rounded-2xl shadow-lg h-fit">
          <h2 className="text-xl font-semibold mb-4">Your Workspace</h2>
          <p className="text-gray-400 text-sm mb-4">Complete the task in the editor below.</p>

          <div className="bg-black rounded-xl overflow-hidden mb-5">
            <img
              src="https://images.unsplash.com/photo-1551033541-2075d8363c66?q=80&w=1920&auto=format&fit=crop"
              alt="Code Editor"
              className="w-full object-cover"
            />
          </div>

          <div className="flex justify-end gap-4">
            <button className="px-5 py-2 rounded-lg bg-gray-700 text-gray-300 hover:bg-gray-600">Save Draft</button>
            <button className="px-5 py-2 rounded-lg bg-teal-500 text-black font-semibold hover:bg-teal-400">
              Submit Assignment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}