```golang
    // main
    ...
    client, err := rpc.DialHTTP("tcp", serverAddress+":1234")
    err = client.Call("Arith.Multiply", args, &reply)
    ...
```


```golang
    // main
    ...
    rpc.Register(arith)
    rpc.HandleHTTP()
    err := http.ListenAndServe(":1234", nil)
    ...

    // Multiply
    func (t *Arith) Multiply(args *Args, reply *int) error {
    ...
    *reply = args.A * args.B
    return nil
    ...
}
```
