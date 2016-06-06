package main

import (
  "bufio"
  "crypto/md5"
  "encoding/hex"
  "fmt"
  "io"
  "net/http"
  "net/url"
  "os"
  "time"
)

func UrlToName(url string) string {
  hasher := md5.New()
  hasher.Write([]byte(url))
  return hex.EncodeToString(hasher.Sum(nil))
}

func Exists(filename string) bool {
  _, err := os.Stat(filename)
  return err == nil
}

func Download(url string) {
  urlname := UrlToName(url)
  filename := "./small_data/html/" + urlname

  if Exists(filename) {
    fmt.Print("Cached ... " + url + " ==> " + filename + "\n")
    time.Sleep(10 * time.Millisecond)
    return
  }

  response, err := http.Get(url)
  if err != nil {
    // panic(err)
    return
  }
  defer response.Body.Close()

  file, err := os.Create(filename)
  if err != nil {
    // panic(err)
    return
  }
  defer file.Close()

  io.Copy(file, response.Body)

  fmt.Print("Fetched ... " + url + " ==> " + filename + "\n")
  time.Sleep(800 * time.Millisecond)
}

func Crawl(c chan string, quit chan bool) {
  for url := range c {
    Download(url)
  }
  quit <- true
}

func MyId(url string) int {
  hash := md5.Sum([]byte(url))
  x := 0
  for i := range hash {
    x = x + int(hash[i])
  }
  return x
}

func main() {
  thread_num := 5000

  urlq := make([]chan string, thread_num)
  quitq := make([]chan bool, thread_num)

  for i := 0; i < thread_num; i++ {
    urlq[i] = make(chan string, 5000)
    quitq[i] = make(chan bool)
  }

  stdin_scan := bufio.NewScanner(os.Stdin)

  for i := range urlq {
    go Crawl(urlq[i], quitq[i])
  }

  for stdin_scan.Scan() {
    inputUrl := stdin_scan.Text()
    u, err := url.Parse(inputUrl)
    if err != nil {
      // TODO something
    } else {
      id := MyId(u.Host) % thread_num
      urlq[id] <- inputUrl
    }
  }

  for i := range urlq {
    close(urlq[i])
  }

  for i := range quitq {
    <-quitq[i]
  }
}
