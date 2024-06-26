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

    job_title = data["data"]["viewer"]["user"]["title"]

    # Match some specific job titles against known role names.
    match job_title:
        case "Director of Engineering":
            current_level = "Director"
        case _:
            current_level = job_title

    current_track = user.track.get_level_by_name(current_level)

    if not current_track:
        raise Exception(
            "Could not find a role within Lattice that matches your job title. "
            "Speak to Kyle or review line 31 in main.py and contribute your "
            "changes :)."
        )
        return

    if not current_track.competencies:
        raise Exception(
            "There are no competencies assigned to your track and role within "
            "Lattice, so there is nothing to export here."
        )
        return

    # Remove " - role requirements" from name because it's ugly :).
    current_track_name = user.track.name.replace(" - role requirements", "")

    export_data = {
        "Competency": [],
        "Status": [],
        "Comments": [],
        "Competency ID": [],
    }

    for competency in current_track.competencies:
        export_data["Competency"].append(competency.name)
        export_data["Competency ID"].append(competency.entity_id)
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
    df.to_excel(output_path, index=False)

    print(f"Spreadsheet saved to: {output_path}")


def main():
    _competencies_export()


if __name__ == "__main__":
    raise SystemExit(main())
