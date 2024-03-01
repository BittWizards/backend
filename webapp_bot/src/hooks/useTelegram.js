const webApp = window.Telegram.WebApp


export function useTelegram() {

    const onClose = () => {
        webApp.close()
    }
    return {
        onClose,
        webApp,
        user: webApp.initDataUnsafe?.user,
    }
}
