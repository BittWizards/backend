import BadgeAvatars from "../components/Avatar/Avatar"


function unpacking_values(data) {
  if (data === null) {
    return ""
  }
  if (typeof(data) === 'string' || typeof(data) === 'integer') {
    return data
  } else
  if (Array.isArray(data)) {
    return (
      <ul>
        {data.map((item, index) => (
          <li key={index}>{item["title"]}</li>
        ))}
      </ul>
    )
  } else if (data !== null) {
    return (
      <>
        {Object.keys(data).map(key => (<>
          <div key={key} style={{ marginLeft: 20, marginBottom: 2 }}>
            <strong>{key}:</strong> {data[key]}
          </div>
        </>))}
      </>
    )
  }
}


export default function Profile ({data}) {

  const newData = { ...data }
  const src = 'https://ambas-1.ddns.net/' + newData["image"]
  delete newData["image"]
  delete newData["id"]

  return (
    <>
      <BadgeAvatars avatar={src}/>
      {Object.keys(newData).map(key => (<>
        <div key={key} style={{ marginLeft: 20, marginBottom: 2 }}>
          <strong>{key}:</strong> {unpacking_values(newData[key])}
        </div>
      </>))}
    </>
  )
}
