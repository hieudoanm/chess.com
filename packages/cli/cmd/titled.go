package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/spf13/cobra"

	"chess-com-cli/data"
	"chess-com-cli/utils/numbers"
	"chess-com-cli/utils/requests"
)

/* ----------------------------- Models ----------------------------- */

type TitledResponse struct {
	Players []string `json:"players"`
}

/* ----------------------------- Helpers ----------------------------- */

func fetchTitleCount(title string) (int, error) {
	url := fmt.Sprintf("https://api.chess.com/pub/titled/%s", title)

	body, err := requests.Get(url, requests.Options{})
	if err != nil {
		return 0, err
	}

	var res TitledResponse
	if err := json.Unmarshal(body, &res); err != nil {
		return 0, err
	}

	return len(res.Players), nil
}

/* ----------------------------- Command ----------------------------- */

var comTitledCmd = &cobra.Command{
	Use:   "titled",
	Short: "Show number of Chess.com players by title",
	Long: `Query Chess.com titled-player endpoints and count players per title.

Titles included:
  GM, WGM, IM, WIM, FM, WFM, NM, WNM, CM, WCM

Example:
  chess-cli com titles`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println()
		fmt.Printf("| %-6s | %7s |\n", "Titled", "Players")
		fmt.Printf("| %-6s | %7s |\n", strings.Repeat("-", 6), strings.Repeat("-", 7))

		for _, title := range data.Titles {
			count, err := fetchTitleCount(title)
			if err != nil {
				fmt.Fprintf(os.Stderr, "❌ Failed to fetch %s: %v\n", title, err)
				continue
			}

			fmt.Printf("| %-6s | %7s |\n", title, numbers.Comma(count))
		}
		fmt.Println()
	},
}

func init() {
	rootCmd.AddCommand(comTitledCmd)
}
