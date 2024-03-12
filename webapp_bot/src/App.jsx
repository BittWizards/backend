import { useEffect, useState } from "react";
import "./App.css";
import { useTelegram } from "./hooks/useTelegram";
import ColorTabs from "./components/Tabs/Tabs";
import Profile from "./pages/Profile";
import Achievements from "./pages/Achievements";

export default function App() {
  const { webApp, user } = useTelegram();
  const [currentTab, setCurrentTab] = useState("profile");
  const [ambassador, setAmbassador] = useState();

  useEffect(() => {
    webApp.ready();
  }, []);

  useEffect(() => {
    if (user) {
      const fetchData = async () => {
        try {
          const response = await fetch(
            "/api/v1/ambassador_by_tg_username/" + user.username
          );
          const jsonData = await response.json();
          setAmbassador(jsonData);
        } catch (error) {
          console.error("Ошибка при получении данных:", error);
        }
      };
      fetchData();
    }
  }, []);

  function onChangeTab(value) {
    setCurrentTab(value);
  }

  return (
    <>
      {user && (
        <>
          <ColorTabs onClick={onChangeTab} currentTab={currentTab} />
          {/* <Header /> */}
          {currentTab === "profile" && <Profile data={ambassador} />}
          {currentTab === "achievements" && <Achievements />}
          {/* {currentTab === "statistic" && <Statistic />} */}
          {/* <button onClick={onToogleButton}>toogle</button> */}
        </>
      )}
    </>
  );
}
