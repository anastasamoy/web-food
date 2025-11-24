import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyChackonCW8g8Xx3DIygcKiLwh-Kx0tLO4",
  authDomain: "web-food-92565.firebaseapp.com",
  projectId: "web-food-92565",
  storageBucket: "web-food-92565.firebasestorage.app",
  messagingSenderId: "464598395264",
  appId: "1:464598395264:web:e78658a4bff90c3bf67965",
  measurementId: "G-YZH9STLYJS"
};

// Инициализация Firebase
const app = initializeApp(firebaseConfig);

// Инициализация Authentication
export const auth = getAuth(app);
export default app;