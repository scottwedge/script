#include "hyzc.h"
#include <arpa/inet.h>
#include <stdio.h>

#define PORT 8000
#define NUM 1024 
#define IP "10.0.200.163"

int main(int args, char *argv[])
{
	char cmd[BUFSIZ] = {0};
	char *p;
	p = cmd;
	int i;
	for(i = 1; i < args;i++){
        strcpy(p, argv[i]);
		p = p + strlen(argv[i]);
		*p = ' ';
		p = p + 1;
	}
	*(--p) = '\n';

    printf("remote execute: %s\n", cmd);	

    int cfd;
	char buf[BUFSIZ] = {0};
	struct sockaddr_in serv_addr;

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	inet_pton(AF_INET, IP, &serv_addr.sin_addr.s_addr);
	cfd = Socket(AF_INET, SOCK_STREAM, 0);

	Connect(cfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));

	write(cfd, cmd, strlen(cmd));
	usleep(100000);
	read(cfd, buf, sizeof(buf));
	printf("remote return \n%s", buf);
	
	Close(cfd);

	return 0;
}

