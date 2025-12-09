import React from "react";
import { Card, CardContent } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { cn } from "../../lib/utils";

const filters = ["All", "High Risk", "Medium Risk", "Low Risk", "On Track"];

const students = [
  {
    name: "Olivia Chen",
    id: "# 452178",
    status: "High Risk",
    statusColor: "bg-red-500/20 text-red-400",
    desc: "Failing Grade in Math. Low attendance over the past 3 weeks.",
    action: "View Plan",
    avatar: "https://i.pravatar.cc/100?img=1",
  },
  {
    name: "Liam Rodriguez",
    id: "# 88142",
    status: "Medium Risk",
    statusColor: "bg-yellow-500/20 text-yellow-300",
    desc: "Several missing assignments in English. Showing signs of disengagement.",
    action: "View Plan",
    avatar: "https://i.pravatar.cc/100?img=2",
  },
  {
    name: "Ava Nguyen",
    id: "# 75430",
    status: "On Track",
    statusColor: "bg-green-500/20 text-green-300",
    desc: "Maintaining excellent grades and attendance. No intervention required.",
    action: "Manage",
    avatar: "https://i.pravatar.cc/100?img=3",
  },
  {
    name: "Noah Kim",
    id: "# 62412",
    status: "Low Risk",
    statusColor: "bg-blue-500/20 text-blue-300",
    desc: "Slight dip in Science quiz scores. Monitoring recommended.",
    action: "View Plan",
    avatar: "https://i.pravatar.cc/100?img=4",
  },
  {
    name: "Isabella Garcia",
    id: "# 30053",
    status: "High Risk",
    statusColor: "bg-red-500/20 text-red-400",
    desc: "Significant behavioural issues reported by multiple teachers.",
    action: "View Plan",
    avatar: "https://i.pravatar.cc/100?img=5",
  },
  {
    name: "Ethan Martinez",
    id: "# 19221",
    status: "Medium Risk",
    statusColor: "bg-yellow-500/20 text-yellow-300",
    desc: "Struggles with homework completion in History class.",
    action: "View Plan",
    avatar: "https://i.pravatar.cc/100?img=6",
  },
];

export default function InterventionsPage() {
  return (
    <div className="min-h-screen bg-[#0D1A2D] text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Interventions</h1>

      <div className="flex items-center gap-4 mb-8">
        <Input placeholder="Search by Student Name or ID..." className="w-72 bg-[#0F223A] text-white border-0" />
        {filters.map((f) => (
          <Button key={f} variant="ghost" className="text-white bg-[#0F223A] px-4 py-2 rounded-xl">
            {f}
          </Button>
        ))}
      </div>

      <div className="grid grid-cols-3 gap-6">
        {students.map((s, i) => (
          <Card key={i} className="bg-[#0F223A] border-0 p-4 rounded-2xl text-white">
            <CardContent>
              <div className="flex items-center gap-3 mb-3">
                <img src={s.avatar} className="w-12 h-12 rounded-full" />
                <div>
                  <p className="font-semibold">{s.name}</p>
                  <p className="text-xs text-gray-400">{s.id}</p>
                </div>
              </div>

              <span className={cn("px-3 py-1 rounded-full text-xs font-medium", s.statusColor)}>
                {s.status}
              </span>

              <p className="text-sm text-gray-300 mt-3 mb-4">{s.desc}</p>

              <Button className="bg-sky-500 w-full text-black font-semibold rounded-xl">
                {s.action}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}