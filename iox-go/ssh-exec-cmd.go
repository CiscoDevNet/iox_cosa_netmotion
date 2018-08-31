package main

 import (
         //"bufio"
         "bytes"
         "fmt"
         "golang.org/x/crypto/ssh"
         //"golang.org/x/crypto/ssh/terminal"
         "net"
         //"os"
         "strings"
	 "gopkg.in/ini.v1"
 )

func Show_cmd_ssh(command string) (string){
	 cfg, err := ini.Load("package_config.ini")



         hostname := cfg.Section("ir_router_info").Key("IP").String()
         port := cfg.Section("ir_router_info").Key("port").String()

         username := cfg.Section("ir_router_info").Key("user").String()
	 password := cfg.Section("ir_router_info").Key("pass").String()
         config := &ssh.ClientConfig{
                 User: username,
                 Auth: []ssh.AuthMethod{ssh.Password(password)},
                 HostKeyCallback: func(hostname string, remote net.Addr, key ssh.PublicKey) error {
                         return nil
                 },
         }
         //fmt.Println("\nConnecting to ", hostname, port)

         hostaddress := strings.Join([]string{hostname, port}, ":")
         client, err := ssh.Dial("tcp", hostaddress, config)
         if err != nil {
                 panic(err.Error())
         }

         session, err := client.NewSession()
         if err != nil {
                 panic(err.Error())
         }
         defer session.Close()

         // fmt.Println("To exit this program, hit Control-C")
         // fmt.Printf("Enter command to execute on %s : ", hostname)

         // fmt.Scanf is unable to accept command with parameters
         // see solution at
         // https://www.socketloop.com/tutorials/golang-accept-input-from-user-with-fmt-scanf-skipped-white-spaces-and-how-to-fix-it
         //fmt.Scanf("%s", &cmd)


         cmd := command
         //log.Printf(cmd)
         //fmt.Println("Executing command ", cmd)

         // capture standard output
         // will NOT be able to handle refreshing output such as TOP command
         // executing top command will result in panic
         var buff bytes.Buffer
         session.Stdout = &buff
         if err := session.Run(cmd); err != nil {
                 panic(err.Error())
         }

         ssh_return := buff.String()
         //fmt.Println(ssh_return)
         session.Close()

         return ssh_return
}

func main() {
        fmt.Println(Show_cmd_ssh("show cell 0/0 all"))
}