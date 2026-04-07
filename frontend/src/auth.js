function deriveUserId(username) {
  let hash = 0;
  for (let i = 0; i < username.length; i++) {
    hash = ((hash << 5) - hash + username.charCodeAt(i)) | 0;
  }
  return Math.abs(hash) % 100000;
}

export function saveSession(username, role) {
  const userId = deriveUserId(username);
  localStorage.setItem("skms_user", JSON.stringify({ username, role, userId }));
}

export function getSession() {
  const raw = localStorage.getItem("skms_user");
  return raw ? JSON.parse(raw) : null;
}

export function clearSession() {
  localStorage.removeItem("skms_user");
}