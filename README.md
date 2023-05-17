# knock knock

## About
Port scanner made with Python and the nmap module. Just runs tcp scans and likely makes a whole hell of a lot of racket, so mostly useful for defense. I use it for testing systems on my home network.

## Important Notes
* Switched from the socket module to nmap. Slows things down a bit but provides a lot more information. 
* Use the `use_default_target` and `default_target_ip` to skip the "input IP" screen. Useful for repeated testing.

## To-Do
- [ ] Verbose mode during scanning.
- [ ] Different scan types with nmap.
- [ ] Save results to a txt file.
- [ ] Re-add the scan w/ the `sockets` module for faster scans.
