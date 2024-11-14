package middleware

import (
	"fmt"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

func APIKeyAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		apiKey := c.GetHeader("X-API-Key")
		fmt.Println("BEOO checkk apiKey",c.GetHeader("X-API-Key"))
		fmt.Println("BEOO checkk API_SECRET_KEY",os.Getenv("API_SECRET_KEY"))
		if apiKey == os.Getenv("API_SECRET_KEY") {
			c.Next()
		} else {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "Unauthorized",
			})
			c.Abort()
		}
	}
}
