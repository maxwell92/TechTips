package main

import (
	"crypto/md5"
	"fmt"
	"html/template"
	"io"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

func sayhelloName(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	fmt.Println(r.Form)
	fmt.Println("path", r.URL.Path)
	fmt.Println("scheme", r.URL.Scheme)
	fmt.Println(r.Form["url_long"])

	for k, v := range r.Form {
		fmt.Println("key:", k)
		fmt.Println("value:", strings.Join(v, ""))
	}

	fmt.Fprintf(w, "Hello mushroom")

}

func login(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()

	fmt.Println("method:", r.Method)
	if r.Method == "GET" {
		crutime := time.Now().Unix()
		h := md5.New()
		io.WriteString(h, strconv.FormatInt(crutime, 10))
		token := fmt.Sprintf("%x", h.Sum(nil))

		fmt.Println(token)

		t, _ := template.ParseFiles("login.gtpl")
		t.Execute(w, token)
	} else {

		if len(r.Form["password"][0]) < 5 {
			fmt.Fprintf(w, "password too short\n")
		}

		if m, _ := regexp.MatchString("^[a-zA-Z]+$", r.Form.Get("username")); !m {
			fmt.Fprintf(w, "username must be English\n")
		}

		if m, _ := regexp.MatchString("^[0-9]+$", r.Form.Get("age")); !m {
			fmt.Fprintf(w, "Age must be number!")
		}

		if m, _ := regexp.MatchString("^\\p{Han}+$", r.Form.Get("realname")); !m {
			fmt.Fprintf(w, "realname must be Chinese!\n")
		}

		if m, _ := regexp.MatchString(`^([\w\.\_]{2, 10})@(\w{1,}).([a-z]{2,4})$`, r.Form.Get("email")); !m {
			fmt.Fprintf(w, "email must be email!\n")
		}

		slice := []string{"apple", "pear", "banana"}
		for _, v := range slice {
			if v == r.Form.Get("fruit") {
				fmt.Fprintln(w, v)
			}
		}

		gslice := []int{1, 2}
		for _, v := range gslice {
			if strconv.Itoa(v) == r.Form.Get("gender") {
				fmt.Fprintln(w, v)
			}
		}

		token := r.Form.Get("token")
		if token != "abc" {
			fmt.Printf("token: %s\n", token)
		} else {
			fmt.Println("token not existed!")
		}

		fmt.Println("username:", r.Form["username"])
		fmt.Println("username length:", len(r.Form["username"][0]))
		fmt.Println("password:", template.HTMLEscapeString(r.Form.Get("password")))
		fmt.Println("age:", r.Form["age"])
		fmt.Println("realname:", r.Form["realname"])
		fmt.Println("email:", r.Form["email"])
	}
}

func upload(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method:", r.Method)
	if r.Method == "GET" {
		crutime := time.Now().Unix()
		h := md5.New()
		io.WriteString(h, strconv.FormatInt(crutime, 10))
		token := fmt.Sprintf("%x", h.Sum(nil))

		t, _ := template.ParseFiles("upload.gtpl")
		t.Execute(w, token)
	} else {
		r.ParseMultipartForm(32 << 20)
		file, handler, err := r.FormFile("uploadfile")
		if err != nil {
			fmt.Println(err)
		}
		defer file.Close()
		fmt.Fprintf(w, "%v", handler.Header)
		f, err := os.OpenFile("./"+handler.Filename, os.O_WRONLY|os.O_CREATE, 0666)
		if err != nil {
			fmt.Println(err)
		}

		defer f.Close()
		io.Copy(f, file)
	}
}

func main() {
	http.HandleFunc("/", sayhelloName)
	http.HandleFunc("/login", login)
	http.HandleFunc("/upload", upload)

	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal("ListenAdnServe:", err)
	}
}
