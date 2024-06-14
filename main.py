from lattice_export import lattice
from lattice_export import types
from dotenv import dotenv_values
from pathlib import Path
import html

import pandas

config = dotenv_values(".env")


def _competencies_export():
    """
    Exports competency data ("Align on expectations" within Lattice) to a
    spreadsheet.
    """

    data = lattice.get_competencies()
    user = types.User.from_dict(data["data"]["user"])

    if not user.track:
        raise Exception(
            "You do not have a track assigned in Lattice, so exporting data "
            "is not possible."
        )
        return

    current_level = data["data"]["viewer"]["user"]["title"]
    current_track = user.track.get_level_by_name(current_level)

    # Remove " - role requirements" from name because it's ugly :).
    current_track_name = user.track.name.replace(" - role requirements", "")

    export_data = {
        "Competencies": [],
        "Status": [],
        "Comments": [],
    }

    for competency in current_track.competencies:
        export_data["Competencies"].append(competency.name)
        export_data["Status"].append(competency.designation)

        competency_comments = ""
        first_comment = True
        for comment in competency.comments:
            # Add a separator between comments if there are multiple.
            if not first_comment:
                competency_comments += "\n\n---------------\n\n"

            # Get latest date.
            comment_date = comment.edited_at or comment.created_at

            # Build comment string so the result is a single string.
            competency_comments += html.unescape(comment.body)
            competency_comments += (
                f"\n\n({comment.commenter.name}, {comment_date.strftime('%Y-%m-%d')})"
            )

            first_comment = False

        # Either add a plain string or the string of comments.
        export_data["Comments"].append(competency_comments)

    # Build export directory.
    output_filename = f"{current_track_name} - {current_level}.xlsx"
    output_dir = Path("./exports")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename

    # Export to spreadsheet.
    df = pandas.DataFrame(export_data)
    df.to_excel(output_path)

    print(f"Spreadsheet saved to: {output_path}")


def main():
    _competencies_export()


if __name__ == "__main__":
    raise SystemExit(main())
