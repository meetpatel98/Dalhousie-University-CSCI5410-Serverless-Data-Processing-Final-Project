export function getValueFromCookie(key){
    let value = document.cookie.match("(^|;)\\s*" + key + "\\s*=\\s*([^;]+)");
    return value ? value.pop() : "";
}

export function getCustomerIdFromCookie(){
    return getValueFromCookie('Customer_Id');
}

export function getAccessTokenFromCookie(){
    return getValueFromCookie('AccessToken');
}