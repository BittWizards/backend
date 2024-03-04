const webApp = window.Telegram.WebApp


export function useTelegram() {

    const onClose = () => {
        webApp.close()
    }

    function onToogleButton() {
        if(webApp.MainButton.isVisible) {
            webApp.MainButton.hide()
        } else {
            webApp.MainButton.show()
        }
    }

    return {
        onClose,
        onToogleButton,
        webApp,
        user: webApp.initDataUnsafe?.user,
    }
}
