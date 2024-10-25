// Copied from HW. Gonna throw it below
"use strict"

function loadPostsGlobal() {                                   //CHANGE
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(xhr)
    }

    console.log("in loadPosts!")
    xhr.open("GET", "/lanturnfly/get-global", true)
    xhr.send()
}

function loadPostsFollow() {                                   //CHANGE
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        updatePage(xhr)
    }

    console.log("in loadPosts!")
    xhr.open("GET", "/lanturnfly/get-follower", true)  
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        updatePosts(response)                           //CHANGE
        return
    }

    console.log("uh oh something went wrong")

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updatePosts(items) {
    let list = document.getElementById(`the_posts_here`);
    // let order

    // if (items[0].id == '1'){
    //     order = items.reverse()
    // }
    // else{
    //     order = items
    // }
    

    items.forEach(item => {
        if (document.getElementById(`id_post_div_${item.id}`) == null) {
            list.prepend(add_commentingBox(item))
            list.prepend(makePostElement(item))
            
            if (item.comments.length > 0){
                updateComments(item)
            }
            
            
            
        }
        else{
            updateComments(item)
        }
    })

    console.log(list)
}

function updateComments(post) {
    let for_post = document.getElementById(`id_post_div_${post.id}`)
    console.log("for_post: ", for_post)

    post.comments.forEach(comment => {
        if (document.getElementById(`id_comment_div_${comment.id}`) == null) {
            for_post.append(makeCommentElement(comment))
        }
    })

    

}

function add_commentingBox(post){
    let commenting_box = 
    `<div class="commenting">
        <label>Comment:</label>
        <input id="id_comment_input_text_${post.id}" type="text">
        <button id="id_comment_button_${post.id}" type="submit" onclick="addComment(${post.id})">Submit</button>
    </div>`
    
    let element = document.createElement("div")
    element.className = 'commenting'

    element.innerHTML = `${commenting_box}`
    return element
}


function makePostElement(post){
    let d = new Date(post.creation_time)
    let time = d.toLocaleDateString() + " " + d.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})
    

    let postInfo = 
    `<a href="other_profile/${post.user_id}" id="id_post_profile_${post.id}">
            Post by ${post.user_first_name} ${post.user_last_name}
        </a> 
        <span>---</span>
        <span id="id_post_text_${post.id}">${sanitize(post.text)}</span>
        <span>---</span>
        <i id="id_post_date_time_${post.id}">${time}</i>  
     ` 


    let element = document.createElement("div")
    element.id = `id_post_div_${post.id}`
    element.className = `post_div`


    element.innerHTML = `${postInfo}`
    return element
}

function makeCommentElement(comment) {

    let d = new Date(comment.creation_time)
    let time = d.toLocaleDateString() + " " + d.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})

    let commentInfo = 
    `<a href="other_profile/${comment.user_id}" id="id_comment_profile_${comment.id}">
        Comment by ${comment.user_first_name} ${comment.user_last_name}
    </a> 
    <span>---</span>
    <span id="id_comment_text_${comment.id}">${sanitize(comment.text)}</span>
    <span>---</span>
    <i id="id_comment_date_time_${comment.id}">${time}</i>
    `

    let element = document.createElement("div")
    element.id = `id_comment_div_${comment.id}`
    element.className = `comment`
    element.innerHTML = `${commentInfo}`

    return element
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function addComment(post_id) {
    let commentTextElement = document.getElementById(`id_comment_input_text_${post_id}`)   //??? idk 
    let commentTextValue = commentTextElement.value

    // Clear input box and old error message (if any)
    commentTextElement.value = ''
    // displayError('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updatePage(xhr)
    }


    xhr.open("POST", addCommentURL, true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`comment_text=${commentTextValue}&csrfmiddlewaretoken=${getCSRFToken()}&post_id=${post_id}`)
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}