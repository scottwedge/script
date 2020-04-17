#include "hyzc.h"

void y_get_radom_array(int *array, int n)
{
	int i;
	unsigned int tm = (unsigned int)time(NULL);
	srand(tm);
	for(i = 0;i < n;i++)
	{
		array[i] = rand() % 100;
	}
}

void y_sys_err(int rvalue, const char *str, int status)
{
	char buf[1024] = {0};
	if(rvalue < 0){
		sprintf(buf, "%s error happen\n", str);
		perror(str);
		exit(status);
	}
}

void pthread_err(int rvalue, const char *str, int status)
{
	char buf[1024] = {0};
	if(rvalue != 0){
		fprintf(stderr, "pthread %s error: %s\n",str, strerror(rvalue));
		exit(status);
	}
}

int Socket(int domain, int type, int protocol)
{
    int fd = socket(domain, type, protocol);
	y_sys_err(fd, "create socket", fd);
	return fd;
}

int Bind(int socket, const struct sockaddr *sa, socklen_t salen)
{
	int n = bind(socket, sa, salen);
	y_sys_err(n, "bind socket", n);
	return n;
}

int Listen(int socket, int back_log)
{
    int n = listen(socket, back_log);
	y_sys_err(n, "listen socket", n);
	return n;
}

int Accept(int socket, struct sockaddr *sa, socklen_t *salenptr)
{
	int n;
again:
	n = accept(socket, sa, salenptr);
	if (n < 0){
        if(( errno == ECONNABORTED) || (errno == EINTR ))
			goto again;
		else
			y_sys_err(n, "accept error", n);
	}
	return n;
}

int Connect(int socket, const struct sockaddr *sa, socklen_t salen)
{
	int n = connect(socket, sa, salen);
	y_sys_err(n, "connect socket", n);
	return n;
}

int Close(int socket)
{
	int n = close(socket);
	y_sys_err(n, "close socket", n);
	return n;
}

ssize_t Read(int fd, void *ptr, size_t nbytes)
{
	ssize_t n;
again:
    n = read(fd, ptr, nbytes);	
	if (n < 0){
		if(errno == EINTR){
			goto again;
		}
	}
	y_sys_err(n, "read socket", n);
	return n;
}

ssize_t Write(int fd, const void *ptr, size_t nbytes)
{
	ssize_t n;
again:
	n = write(fd, ptr, nbytes);
	if (n < 0){
		if(errno == EINTR){
			goto again;
		}
	}
	y_sys_err(n, "write socket", n);
	return n;
}

ssize_t Readn(int fd, void *vptr, size_t nbytes)
{
	size_t nleft;
	ssize_t nread;
	char *ptr;
	ptr = vptr;
	nleft = nbytes;
	while(nleft > 0){
		nread = read(fd, ptr, nleft);
		if(nread < 0){
			if(errno == EINTR){
				nread = 0;
			}
            else{
			    return -1;
			}
		}
	    else if(nread == 0){
			break;
		}
		else{
			nleft -= nread;
			ptr += nread;
		}
	}
	return nbytes - nleft;
}

ssize_t Writen(int fd, const void *vptr, size_t n)
{
	size_t nleft;
	ssize_t nwritten;
	const char *ptr;

	ptr = vptr;
	nleft = n;
	while (nleft > 0) {
		if ( (nwritten = write(fd, ptr, nleft)) <= 0) {
			if (nwritten < 0 && errno == EINTR)
				nwritten = 0;
			else
				return -1;
		}

		nleft -= nwritten;
		ptr += nwritten;
	}
	return n;
}

static ssize_t my_read(int fd, char *ptr)
{
	static int read_cnt;
	static char *read_ptr;
	static char read_buf[100];

	if (read_cnt <= 0) {
again:
		if ( (read_cnt = read(fd, read_buf, sizeof(read_buf))) < 0) {
			if (errno == EINTR)
				goto again;
			return -1;
		} else if (read_cnt == 0)
			return 0;
		read_ptr = read_buf;
	}
	read_cnt--;
	*ptr = *read_ptr++;

	return 1;
}

ssize_t Readline(int fd, void *vptr, size_t maxlen)
{
	ssize_t n, rc;
	char    c, *ptr;

	ptr = vptr;
	for (n = 1; n < maxlen; n++) {
		if ( (rc = my_read(fd, &c)) == 1) {
			*ptr++ = c;
			if (c  == '\n')
				break;
		} else if (rc == 0) {
			*ptr = 0;
			return n - 1;
		} else
			return -1;
	}
	*ptr  = 0;

	return n;
}


