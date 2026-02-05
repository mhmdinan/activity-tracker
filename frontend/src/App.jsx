import { useEffect, useState } from "react";
import { fetchActivities, getActivityPlot, logActivity } from "./api";
import { Activity, BarChart3, PlusCircle, Plus} from 'lucide-react';


export default function App() {
  const [activities, setActivities] = useState([]);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [graphBase64, setGraphBase64] = useState("");
  const [inputCount, setInputCount] = useState(0);

  useEffect(() => {
    loadActivities();
  }, []);

  const loadActivities = async () => {
    const res = await fetchActivities(0, 20);
    console.log("Data from API: ", res.data);
    setActivities(res.data);
  }

  const handleLog = async (activity_name) => {
    await logActivity(activity_name, inputCount);
    alert("Logged successfully");
    if (selectedActivity === activity_name) loadGraph(activity_name);
  };

  const loadGraph = async (activity_name) => {
    setSelectedActivity(activity_name);
    const res = await getActivityPlot(activity_name, 7);
    setGraphBase64(res.data.image);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <header className="mb-8 border-b pb-4">
        <h1 className="text-3xl font-bold text-indigo-600 flex items-center gap-2">
          <Activity /> Activity Tracker
        </h1>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section className="space-y-6">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <PlusCircle size={20}/> Log Activity
          </h2>

          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <input 
            type="number"
            placeholder="Amount (e.g. 10)"
            className="border rounded p-2 mr-2"
            onChange={(e) => setInputCount(Number(e.target.value))}
            />
            <div className="mt-4 grid grid-cols-2 gap-2">
              {activities?.map(act => (
                <button
                key={act.id}
                onClick={() => handleLog(act.name)}
                className="bg-indigo-50 text-indigo-700 p-2 rounded hover:bg-indigo-100 transition"
                >
                  + {act.name}
                </button>
              ))}
            </div>
          </div>
        </section>

        <section className="space-y-6">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <BarChart3 size={20}/>Analytics
            </h2>
          <div className="bg-white p-6 rounded-xl shadow-sm border min-h-[300px] flex flex-col items-center justify-center">
            {graphBase64 ? (
              <img src={graphBase64} alt="Progress Graph" className="w-full rounded"/>
            ) : (
              <p className="text-gray-400">Select an activty from the list to view progress</p>
            )}
            <div className="mt-4 flex gap-2">
              {activities?.map(act => (
                <button
                key={act.id}
                onClick={() => loadGraph(act.name)}
                className={`px-3 py-1 rounded-full text-sm ${selectedActivity === act.name ? 'bg-indigo-600 text-white' : 'bg-gray-200'}`}
                >
                  {act.name}
                </button>
              ))}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

