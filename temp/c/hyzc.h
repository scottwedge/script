#ifndef _HYZC_H_

#define _HYZC_H_
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <errno.h>

void y_get_radom_array(int *array, int n);
void y_sys_err(int rvalue, const char *str, int status);
void y_thread_err(int rvalue, const char *str, int status);

int Socket(int domain, int type, int protocol);
int Bind(int socket, const struct sockaddr *sa, socklen_t salen);
int Listen(int socket, int back_log);
int Accept(int socket, struct sockaddr * sa, socklen_t *salenptr);
int Connect(int socket, const struct sockaddr *sa, socklen_t salen);
int Close(int socket);
ssize_t Read(int fd, void *ptr, size_t nbytes);
ssize_t Write(int fd, const void *ptr, size_t nbytes);
ssize_t Readn(int fd, void *vptr, size_t nbytes);
ssize_t Writen(int fd, const void *vptr, size_t n);
static ssize_t my_read(int fd, char *ptr);
ssize_t Readline(int fd, void *vptr, size_t maxlen);
#endif
