import BadgeAvatars from "../components/Avatar/Avatar"


export default function Profile ({data}) {

  const newData = { ...data }
  const src = 'https://ambas-1.ddns.net/' + newData["image"]
  delete newData["image"]
  delete newData["id"]

  console.log(src)

  return (
    <>
      <BadgeAvatars avatar={src}/>
      {Object.keys(newData).map(key => (<>
        <div key={key} style={{ marginLeft: 20, marginBottom: 2 }}>
          <strong>{key}:</strong> {newData[key]}
        </div>
      </>))}
    </>
  )
}
